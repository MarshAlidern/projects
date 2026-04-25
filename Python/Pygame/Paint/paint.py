import pygame
import sys
import math

TOOLBAR_W = 64
W, H      = 900, 640
CANVAS_X  = TOOLBAR_W
CANVAS_W  = W - TOOLBAR_W
FPS       = 60

BG_TOOLBAR  = (30,  30,  35)
BG_CANVAS   = (255, 255, 255)
ACCENT      = (90, 180, 255)
TEXT_COL    = (200, 205, 215)
HOVER_COL   = (50,  52,  60)
SEL_COL     = (60,  62,  75)

PALETTE = [
    (0,   0,   0),   (255, 255, 255),
    (200, 30,  30),  (230, 100, 30),
    (220, 200, 20),  (40,  180, 40),
    (30,  130, 220), (100, 40,  200),
    (220, 80,  160), (120, 70,  40),
    (160, 160, 160), (80,  80,  80),
]


TOOLS = ["pencil", "eraser", "line", "rect", "circle", "fill"]

ICONS = {
    "pencil": [ 
        ((20, 44), (32, 20)), ((32, 20), (36, 24)), ((36, 24), (24, 48)),
        ((20, 44), (24, 48)),
    ],
    "eraser": None,  
    "line":   [((16, 48), (48, 16))],
    "rect":   None,
    "circle": None,
    "fill":   None,
}

def flood_fill(surface, pos, new_color):
    x, y = pos
    target = surface.get_at((x, y))[:3]
    if target == new_color[:3]:
        return
    stack = [(x, y)]
    visited = set()
    w, h = surface.get_size()
    while stack:
        cx, cy = stack.pop()
        if (cx, cy) in visited:
            continue
        if not (0 <= cx < w and 0 <= cy < h):
            continue
        if surface.get_at((cx, cy))[:3] != target:
            continue
        visited.add((cx, cy))
        surface.set_at((cx, cy), new_color)
        stack += [(cx+1,cy),(cx-1,cy),(cx,cy+1),(cx,cy-1)]

def draw_icon(surf, tool, rect, color):
    cx, cy = rect.centerx, rect.centery
    r = rect

    if tool == "pencil":
     
        pts = [(cx-8, cy+12),(cx+4,cy-12),(cx+8,cy-8),(cx-4,cy+16)]
        pygame.draw.polygon(surf, color, pts, 2)
    
        pygame.draw.circle(surf, color, (cx-5, cy+13), 2)

    elif tool == "eraser":
        pygame.draw.rect(surf, color,
                         pygame.Rect(cx-10, cy-6, 20, 14), 2, border_radius=3)
        pygame.draw.line(surf, color, (cx-4, cy-6), (cx-4, cy+8), 2)

    elif tool == "line":
        pygame.draw.line(surf, color, (cx-10, cy+10), (cx+10, cy-10), 2)

    elif tool == "rect":
        pygame.draw.rect(surf, color,
                         pygame.Rect(cx-10, cy-8, 20, 16), 2)

    elif tool == "circle":
        pygame.draw.circle(surf, color, (cx, cy), 10, 2)

    elif tool == "fill":
  
        pts = [(cx-8,cy+8),(cx-4,cy+12),(cx+6,cy+2),(cx+2,cy-2)]
        pygame.draw.polygon(surf, color, pts, 2)
        pygame.draw.circle(surf, color, (cx+6, cy-8), 5, 2)
        pygame.draw.line(surf, color, (cx-2, cy-2), (cx+1, cy-6), 2)


class Paint:
    def __init__(self):
        pygame.init()
        self.screen  = pygame.display.set_mode((W, H))
        pygame.display.set_caption("Paint")
        self.clock   = pygame.time.Clock()

        self.canvas   = pygame.Surface((CANVAS_W, H))
        self.canvas.fill(BG_CANVAS)

        self.tool     = "pencil"
        self.color    = (0, 0, 0)
        self.size     = 4        
        self.drawing  = False
        self.start    = None    
        self.preview  = None     

        self._build_toolbar()


    def _build_toolbar(self):
        PAD = 8
        self.tool_rects  = {}
        self.color_rects = {}
        self.size_rects  = {}

        y = PAD
        for t in TOOLS:
            r = pygame.Rect(PAD, y, TOOLBAR_W - PAD*2, TOOLBAR_W - PAD*2)
            self.tool_rects[t] = r
            y += TOOLBAR_W - PAD + 2

        y += 4

        sw = (TOOLBAR_W - PAD*2 - 2) // 2
        for i, c in enumerate(PALETTE):
            col = i % 2
            row = i // 2
            r = pygame.Rect(PAD + col*(sw+2), y + row*(sw+2), sw, sw)
            self.color_rects[i] = (r, c)

        y2 = y + (len(PALETTE)//2) * (sw+2) + 10
        self.size_rects = {}
        for i, s in enumerate([2, 4, 8, 16]):
            r = pygame.Rect(PAD + i*14, y2, 12, 12)
            self.size_rects[s] = r
        self.size_y = y2

    def canvas_pos(self, screen_pos):
        x, y = screen_pos
        return (x - CANVAS_X, y)

    def in_canvas(self, screen_pos):
        return screen_pos[0] >= CANVAS_X

    def draw_toolbar(self):
        s = self.screen
        pygame.draw.rect(s, BG_TOOLBAR, (0, 0, TOOLBAR_W, H))

        for t, r in self.tool_rects.items():
            bg = SEL_COL if t == self.tool else BG_TOOLBAR
            pygame.draw.rect(s, bg, r, border_radius=6)
            if t == self.tool:
                pygame.draw.rect(s, ACCENT, r, 1, border_radius=6)
            ic = ACCENT if t == self.tool else TEXT_COL
            draw_icon(s, t, r, ic)

        for i, (r, c) in self.color_rects.items():
            pygame.draw.rect(s, c, r, border_radius=2)
            if c == self.color:
                pygame.draw.rect(s, ACCENT, r, 2, border_radius=2)

        for sz, r in self.size_rects.items():
            col = ACCENT if sz == self.size else TEXT_COL
            pygame.draw.rect(s, col, r, border_radius=3)


    def draw_canvas(self):
        self.screen.blit(self.canvas, (CANVAS_X, 0))

        if self.drawing and self.start and self.tool in ("line","rect","circle"):
            mp = pygame.mouse.get_pos()
            cp = self.canvas_pos(mp)
            tmp = self.canvas.copy()
            self._draw_shape(tmp, self.tool, self.start, cp, self.color, self.size)
            self.screen.blit(tmp, (CANVAS_X, 0))

    def _draw_shape(self, surf, tool, p1, p2, color, size):
        if tool == "line":
            pygame.draw.line(surf, color, p1, p2, size)
        elif tool == "rect":
            x = min(p1[0], p2[0]); y = min(p1[1], p2[1])
            w = abs(p2[0]-p1[0]);  h = abs(p2[1]-p1[1])
            pygame.draw.rect(surf, color, (x, y, max(1,w), max(1,h)), size)
        elif tool == "circle":
            rx = abs(p2[0]-p1[0])//2; ry = abs(p2[1]-p1[1])//2
            cx = (p1[0]+p2[0])//2;    cy = (p1[1]+p2[1])//2
            r  = max(1, max(rx, ry))
            pygame.draw.circle(surf, color, (cx, cy), r, size)


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()


            if event.type == pygame.KEYDOWN:
                keys = {'p':'pencil','e':'eraser','l':'line',
                        'r':'rect','c':'circle','f':'fill'}
                if event.unicode in keys:
                    self.tool = keys[event.unicode]
                if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    self.canvas.fill(BG_CANVAS)

                if event.key == pygame.K_LEFTBRACKET:
                    sizes = list(self.size_rects); i = sizes.index(self.size)
                    self.size = sizes[max(0, i-1)]
                if event.key == pygame.K_RIGHTBRACKET:
                    sizes = list(self.size_rects); i = sizes.index(self.size)
                    self.size = sizes[min(len(sizes)-1, i+1)]


            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mp = event.pos


                for t, r in self.tool_rects.items():
                    if r.collidepoint(mp):
                        self.tool = t

                for i, (r, c) in self.color_rects.items():
                    if r.collidepoint(mp):
                        self.color = c

                for sz, r in self.size_rects.items():
                    if r.collidepoint(mp):
                        self.size = sz


                if self.in_canvas(mp):
                    cp = self.canvas_pos(mp)
                    self.drawing = True
                    self.start   = cp

                    if self.tool == "pencil":
                        pygame.draw.circle(self.canvas, self.color, cp, self.size//2)
                    elif self.tool == "eraser":
                        pygame.draw.circle(self.canvas, BG_CANVAS, cp, self.size)
                    elif self.tool == "fill":
                        flood_fill(self.canvas, cp, self.color)
                        self.drawing = False


            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.drawing and self.start:
                    mp = event.pos
                    if self.in_canvas(mp):
                        cp = self.canvas_pos(mp)
                        if self.tool in ("line","rect","circle"):
                            self._draw_shape(self.canvas, self.tool,
                                             self.start, cp, self.color, self.size)
                self.drawing = False
                self.start   = None

            if event.type == pygame.MOUSEMOTION and self.drawing:
                mp = event.pos
                if self.in_canvas(mp):
                    cp = self.canvas_pos(mp)
                    if self.tool == "pencil":
                        prev = self.canvas_pos(
                            (mp[0]-event.rel[0], mp[1]-event.rel[1]))
                        pygame.draw.line(self.canvas, self.color,
                                         prev, cp, self.size)
                    elif self.tool == "eraser":
                        pygame.draw.circle(self.canvas, BG_CANVAS,
                                           cp, self.size)

    def run(self):
        font = pygame.font.SysFont("Courier New", 11)

        while True:
            self.handle_events()
            self.screen.fill((18, 18, 22))
            self.draw_canvas()
            self.draw_toolbar()


            pygame.draw.line(self.screen, (55,55,65),
                             (TOOLBAR_W, 0), (TOOLBAR_W, H))


            hint = f"{self.tool}  [{self.size}px]  Del=clear"
            txt  = font.render(hint, True, (90, 95, 110))
            self.screen.blit(txt, (CANVAS_X + 6, H - 16))

            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    Paint().run()
