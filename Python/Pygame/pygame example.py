import pygame
import sys
import math
import copy

pygame.init()

# ── Constants ──────────────────────────────────────────────────────────────────
INIT_W, INIT_H = 1100, 720
TOOLBAR_W = 72
MIN_W, MIN_H = 700, 500

# Palette
COLORS = {
    "red":    (220,  50,  50),
    "blue":   ( 50, 100, 220),
    "yellow": (240, 200,  30),
    "black":  ( 20,  20,  20),
}
WHITE   = (255, 255, 255)
BG_DARK = ( 28,  28,  36)
PANEL   = ( 38,  38,  50)
ACCENT  = (100, 200, 255)
HOVER   = ( 55,  55,  72)
SELECTED_OUTLINE = (100, 200, 255)

TOOLS = ["pencil", "eraser", "bucket", "rect", "circle"]
TOOL_ICONS = {
    "pencil": "✏",
    "eraser": "⬜",
    "bucket": "🪣",
    "rect":   "▭",
    "circle": "○",
}

# ── Helpers ────────────────────────────────────────────────────────────────────

def draw_rounded_rect(surf, color, rect, r=8):
    pygame.draw.rect(surf, color, rect, border_radius=r)

def lerp_color(a, b, t):
    return tuple(int(a[i] + (b[i]-a[i])*t) for i in range(3))

# ── Shape object ───────────────────────────────────────────────────────────────

class Shape:
    def __init__(self, kind, color, cx, cy, w, h, angle=0.0):
        self.kind   = kind   # "rect" | "circle"
        self.color  = color
        self.cx     = cx
        self.cy     = cy
        self.w      = max(10, w)
        self.h      = max(10, h)
        self.angle  = angle  # degrees

    def bounding_rect(self):
        return pygame.Rect(self.cx - self.w//2, self.cy - self.h//2, self.w, self.h)

    def hit_test(self, x, y):
        """Test in local (un-rotated) space."""
        dx = x - self.cx
        dy = y - self.cy
        rad = -math.radians(self.angle)
        lx = dx*math.cos(rad) - dy*math.sin(rad)
        ly = dx*math.sin(rad) + dy*math.cos(rad)
        if self.kind == "rect":
            return abs(lx) <= self.w/2 and abs(ly) <= self.h/2
        else:
            return (lx/(self.w/2))**2 + (ly/(self.h/2))**2 <= 1.0

    def draw(self, surf, selected=False):
        # Render onto a temp surface, then rotate
        pad = 4
        sw = self.w + pad*2 + 2
        sh = self.h + pad*2 + 2
        tmp = pygame.Surface((sw, sh), pygame.SRCALPHA)
        cx, cy = sw//2, sh//2
        if self.kind == "rect":
            pygame.draw.rect(tmp, self.color, (pad, pad, self.w, self.h))
            if selected:
                pygame.draw.rect(tmp, SELECTED_OUTLINE,
                                 (pad-2, pad-2, self.w+4, self.h+4), 2)
        else:
            pygame.draw.ellipse(tmp, self.color, (pad, pad, self.w, self.h))
            if selected:
                pygame.draw.ellipse(tmp, SELECTED_OUTLINE,
                                    (pad-2, pad-2, self.w+4, self.h+4), 2)
        rotated = pygame.transform.rotate(tmp, self.angle)
        rr = rotated.get_rect(center=(self.cx, self.cy))
        surf.blit(rotated, rr.topleft)

        if selected:
            self._draw_handles(surf)

    def _draw_handles(self, surf):
        handles = self._handle_positions()
        for name, (hx, hy) in handles.items():
            if name == "rotate":
                pygame.draw.circle(surf, (255, 220, 60), (int(hx), int(hy)), 7)
                pygame.draw.circle(surf, (0,0,0),        (int(hx), int(hy)), 7, 2)
            else:
                r = pygame.Rect(int(hx)-5, int(hy)-5, 10, 10)
                pygame.draw.rect(surf, SELECTED_OUTLINE, r, border_radius=3)
                pygame.draw.rect(surf, (0,0,0), r, 1, border_radius=3)

    def _handle_positions(self):
        rad = math.radians(self.angle)
        cos_a, sin_a = math.cos(rad), math.sin(rad)
        def rot(dx, dy):
            return (self.cx + dx*cos_a - dy*sin_a,
                    self.cy + dx*sin_a + dy*cos_a)
        hw, hh = self.w/2, self.h/2
        return {
            "tl": rot(-hw, -hh),
            "tr": rot( hw, -hh),
            "bl": rot(-hw,  hh),
            "br": rot( hw,  hh),
            "rotate": rot(0, -hh - 24),
        }

    def handle_hit(self, x, y, tol=10):
        for name, (hx, hy) in self._handle_positions().items():
            if math.hypot(x-hx, y-hy) < tol:
                return name
        return None

# ── Flood fill (canvas pixels) ─────────────────────────────────────────────────

def flood_fill(surface, x, y, fill_color):
    target = surface.get_at((x, y))[:3]
    if target == fill_color[:3]:
        return
    w, h = surface.get_size()
    pixels = pygame.surfarray.pixels2d(surface)
    target_px = surface.map_rgb(*target)
    fill_px   = surface.map_rgb(*fill_color)
    stack = [(x, y)]
    visited = set()
    while stack:
        cx, cy = stack.pop()
        if (cx, cy) in visited: continue
        if cx < 0 or cx >= w or cy < 0 or cy >= h: continue
        if pixels[cx][cy] != target_px: continue
        visited.add((cx, cy))
        pixels[cx][cy] = fill_px
        stack += [(cx+1,cy),(cx-1,cy),(cx,cy+1),(cx,cy-1)]
    del pixels

# ── Main App ───────────────────────────────────────────────────────────────────

class PaintApp:
    def __init__(self):
        self.screen = pygame.display.set_mode((INIT_W, INIT_H), pygame.RESIZABLE)
        pygame.display.set_caption("PyPaint")
        self.clock  = pygame.time.Clock()

        self.tool      = "pencil"
        self.color     = COLORS["black"]
        self.brush_sz  = 6
        self.drawing   = False
        self.last_pos  = None

        # Canvas
        self.canvas_w = INIT_W - TOOLBAR_W
        self.canvas_h = INIT_H
        self.canvas   = pygame.Surface((self.canvas_w, self.canvas_h))
        self.canvas.fill(WHITE)

        # Shapes layer
        self.shapes   : list[Shape] = []
        self.selected : Shape | None = None
        self.drag_mode   = None   # None | "move" | handle name
        self.drag_origin = None   # (mx, my)
        self.shape_origin= None   # snapshot of shape at drag start
        self.preview_shape: Shape | None = None
        self.shape_start = None

        # Undo
        self.undo_stack = []
        self._push_undo()

        # UI state
        self.hovered_tool  = None
        self.hovered_color = None

        # Fonts
        self.font_icon = pygame.font.SysFont("segoe ui emoji", 22)
        self.font_sm   = pygame.font.SysFont("consolas", 11)
        self.font_md   = pygame.font.SysFont("consolas", 13, bold=True)

    # ── Undo ──────────────────────────────────────────────────────────────────

    def _push_undo(self):
        snap_canvas = self.canvas.copy()
        snap_shapes = copy.deepcopy(self.shapes)
        self.undo_stack.append((snap_canvas, snap_shapes))
        if len(self.undo_stack) > 40:
            self.undo_stack.pop(0)

    def undo(self):
        if len(self.undo_stack) > 1:
            self.undo_stack.pop()
            self.canvas, self.shapes = self.undo_stack[-1]
            self.canvas = self.canvas.copy()
            self.shapes = copy.deepcopy(self.shapes)
            self.selected = None

    # ── Canvas geometry ───────────────────────────────────────────────────────

    def canvas_rect(self):
        sw, sh = self.screen.get_size()
        return pygame.Rect(TOOLBAR_W, 0, sw - TOOLBAR_W, sh)

    def to_canvas(self, mx, my):
        return (mx - TOOLBAR_W, my)

    # ── Drawing ───────────────────────────────────────────────────────────────

    def draw_stroke(self, x, y):
        if self.last_pos:
            col = WHITE if self.tool == "eraser" else self.color
            sz  = self.brush_sz * (4 if self.tool == "eraser" else 1)
            pygame.draw.line(self.canvas, col, self.last_pos, (x, y), sz*2)
            pygame.draw.circle(self.canvas, col, (x, y), sz)
        self.last_pos = (x, y)

    # ── Toolbar layout ────────────────────────────────────────────────────────

    def _tool_rect(self, i):
        return pygame.Rect(8, 60 + i*56, 56, 46)

    def _color_rect(self, i):
        return pygame.Rect(14, 60 + len(TOOLS)*56 + 20 + i*46, 44, 36)

    def _brush_rect(self):
        sw, sh = self.screen.get_size()
        return pygame.Rect(14, sh - 90, 44, 30)

    # ── Render ────────────────────────────────────────────────────────────────

    def render(self):
        sw, sh = self.screen.get_size()
        self.screen.fill(BG_DARK)

        # Canvas
        cr = self.canvas_rect()
        # Resize canvas if window resized
        if self.canvas.get_size() != (cr.w, cr.h):
            new_c = pygame.Surface((cr.w, cr.h))
            new_c.fill(WHITE)
            new_c.blit(self.canvas, (0, 0))
            self.canvas = new_c
        self.screen.blit(self.canvas, (TOOLBAR_W, 0))

        # Shapes
        for s in self.shapes:
            s.draw(self.screen, selected=(s is self.selected))

        # Preview shape while drawing
        if self.preview_shape:
            self.preview_shape.draw(self.screen)

        # Toolbar panel
        draw_rounded_rect(self.screen, PANEL, pygame.Rect(0, 0, TOOLBAR_W, sh), r=0)
        pygame.draw.line(self.screen, (60, 60, 80), (TOOLBAR_W, 0), (TOOLBAR_W, sh), 2)

        # App title
        title = self.font_md.render("PAINT", True, ACCENT)
        self.screen.blit(title, (TOOLBAR_W//2 - title.get_width()//2, 14))

        # Tool buttons
        color_names = list(COLORS.keys())
        for i, t in enumerate(TOOLS):
            r = self._tool_rect(i)
            is_sel = self.tool == t
            is_hov = self.hovered_tool == t
            bg = lerp_color(PANEL, HOVER, 0.5) if is_hov and not is_sel else PANEL
            if is_sel:
                bg = lerp_color(ACCENT, (60, 60, 80), 0.5)
            draw_rounded_rect(self.screen, bg, r, r=8)
            if is_sel:
                pygame.draw.rect(self.screen, ACCENT, r, 2, border_radius=8)

            icon = self.font_icon.render(TOOL_ICONS[t], True, WHITE if not is_sel else ACCENT)
            self.screen.blit(icon, (r.centerx - icon.get_width()//2,
                                    r.y + 4))
            lbl = self.font_sm.render(t, True, (160,160,200) if not is_sel else ACCENT)
            self.screen.blit(lbl, (r.centerx - lbl.get_width()//2, r.bottom - 14))

        # Color swatches
        cy_start = 60 + len(TOOLS)*56 + 20
        lbl = self.font_sm.render("COLOR", True, (120,120,160))
        self.screen.blit(lbl, (TOOLBAR_W//2 - lbl.get_width()//2, cy_start - 14))
        for i, (name, col) in enumerate(COLORS.items()):
            r = self._color_rect(i)
            is_hov = self.hovered_color == name
            draw_rounded_rect(self.screen, col, r, r=6)
            if self.color == col:
                pygame.draw.rect(self.screen, WHITE, r, 3, border_radius=6)
            elif is_hov:
                pygame.draw.rect(self.screen, (200,200,200), r, 2, border_radius=6)

        # Brush size
        br = self._brush_rect()
        lbl = self.font_sm.render("SIZE", True, (120,120,160))
        self.screen.blit(lbl, (TOOLBAR_W//2 - lbl.get_width()//2, br.y - 16))
        draw_rounded_rect(self.screen, HOVER, br, r=6)
        sz_txt = self.font_md.render(str(self.brush_sz), True, WHITE)
        self.screen.blit(sz_txt, (br.centerx - sz_txt.get_width()//2,
                                   br.centery - sz_txt.get_height()//2))
        # +/- arrows
        minus = self.font_md.render("-", True, ACCENT)
        plus  = self.font_md.render("+", True, ACCENT)
        self.screen.blit(minus, (br.x - 1, br.centery - minus.get_height()//2))
        self.screen.blit(plus,  (br.right - plus.get_width() - 1,
                                  br.centery - plus.get_height()//2))

        # Undo hint
        hint = self.font_sm.render("Ctrl+Z", True, (100,100,130))
        self.screen.blit(hint, (TOOLBAR_W//2 - hint.get_width()//2, sh - 30))

        pygame.display.flip()

    # ── Events ────────────────────────────────────────────────────────────────

    def handle_event(self, event):
        sw, sh = self.screen.get_size()

        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z and (event.mod & pygame.KMOD_CTRL):
                self.undo()
            if event.key == pygame.K_DELETE and self.selected:
                self.shapes.remove(self.selected)
                self.selected = None
                self._push_undo()

        if event.type == pygame.VIDEORESIZE:
            pass  # RESIZABLE handles it automatically

        if event.type == pygame.MOUSEMOTION:
            mx, my = event.pos
            self._update_hover(mx, my)

            if self.drawing and self.tool in ("pencil", "eraser"):
                cx, cy = self.to_canvas(mx, my)
                cr = self.canvas_rect()
                if 0 <= cx < cr.w and 0 <= cy < cr.h:
                    self.draw_stroke(cx, cy)

            elif self.tool in ("rect", "circle") and self.shape_start and not self.selected:
                cx, cy = self.to_canvas(mx, my)
                sx, sy = self.shape_start
                w = abs(cx - sx)
                h = abs(cy - sy)
                pcx = (sx + cx) // 2 + TOOLBAR_W
                pcy = (sy + cy) // 2
                self.preview_shape = Shape(self.tool, self.color, pcx, pcy, w, h)

            elif self.drag_mode and self.selected:
                self._do_drag(mx, my)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if event.button == 1:
                self._mouse_down(mx, my)
            if event.button == 4:  # scroll up → brush bigger
                self.brush_sz = min(40, self.brush_sz + 1)
            if event.button == 5:  # scroll down → brush smaller
                self.brush_sz = max(1, self.brush_sz - 1)

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self._mouse_up(*event.pos)

        return True

    def _update_hover(self, mx, my):
        self.hovered_tool  = None
        self.hovered_color = None
        if mx < TOOLBAR_W:
            for i, t in enumerate(TOOLS):
                if self._tool_rect(i).collidepoint(mx, my):
                    self.hovered_tool = t
            for i, name in enumerate(COLORS.keys()):
                if self._color_rect(i).collidepoint(mx, my):
                    self.hovered_color = name

    def _mouse_down(self, mx, my):
        # Toolbar clicks
        if mx < TOOLBAR_W:
            for i, t in enumerate(TOOLS):
                if self._tool_rect(i).collidepoint(mx, my):
                    self.tool = t
                    self.selected = None
                    return
            for i, (name, col) in enumerate(COLORS.items()):
                if self._color_rect(i).collidepoint(mx, my):
                    self.color = col
                    return
            br = self._brush_rect()
            if br.collidepoint(mx, my):
                if mx < br.centerx:
                    self.brush_sz = max(1, self.brush_sz - 1)
                else:
                    self.brush_sz = min(40, self.brush_sz + 1)
            return

        # Canvas area
        cx, cy = self.to_canvas(mx, my)

        if self.tool in ("pencil", "eraser"):
            self.selected = None
            self.drawing  = True
            self.last_pos = None
            self.draw_stroke(cx, cy)
            return

        if self.tool == "bucket":
            self.selected = None
            cr = self.canvas_rect()
            if 0 <= cx < cr.w and 0 <= cy < cr.h:
                self._push_undo()
                flood_fill(self.canvas, cx, cy, self.color)
            return

        if self.tool in ("rect", "circle"):
            # Check if clicking on existing selected shape handle
            if self.selected:
                handle = self.selected.handle_hit(mx, my)
                if handle:
                    self.drag_mode    = handle
                    self.drag_origin  = (mx, my)
                    self.shape_origin = copy.copy(self.selected)
                    return
                # Click inside shape → move
                if self.selected.hit_test(mx, my):
                    self.drag_mode    = "move"
                    self.drag_origin  = (mx, my)
                    self.shape_origin = copy.copy(self.selected)
                    return

            # Check all shapes (back-to-front)
            hit = None
            for s in reversed(self.shapes):
                if s.hit_test(mx, my):
                    hit = s
                    break
            if hit:
                self.selected     = hit
                self.drag_mode    = "move"
                self.drag_origin  = (mx, my)
                self.shape_origin = copy.copy(hit)
                return

            # Start drawing new shape
            self.selected    = None
            self.shape_start = (cx, cy)
            self.preview_shape = None

    def _mouse_up(self, mx, my):
        if self.tool in ("pencil", "eraser") and self.drawing:
            self.drawing   = False
            self.last_pos  = None
            self._push_undo()
            return

        if self.tool in ("rect", "circle"):
            if self.drag_mode and self.selected:
                self.drag_mode    = None
                self.drag_origin  = None
                self.shape_origin = None
                self._push_undo()
                return

            if self.shape_start:
                cx, cy = self.to_canvas(mx, my)
                sx, sy = self.shape_start
                w = abs(cx - sx)
                h = abs(cy - sy)
                if w > 4 and h > 4:
                    pcx = (sx + cx) // 2 + TOOLBAR_W
                    pcy = (sy + cy) // 2
                    s = Shape(self.tool, self.color, pcx, pcy, w, h)
                    self.shapes.append(s)
                    self.selected = s
                    self._push_undo()
                self.shape_start   = None
                self.preview_shape = None

    def _do_drag(self, mx, my):
        if not self.selected or not self.drag_origin:
            return
        dx = mx - self.drag_origin[0]
        dy = my - self.drag_origin[1]
        s  = self.selected
        o  = self.shape_origin

        if self.drag_mode == "move":
            s.cx = o.cx + dx
            s.cy = o.cy + dy

        elif self.drag_mode == "rotate":
            # Angle from center to mouse
            angle = math.degrees(math.atan2(my - s.cy, mx - s.cx))
            s.angle = angle + 90

        elif self.drag_mode in ("tl","tr","bl","br"):
            # Scale: use distance from center
            dist_now  = math.hypot(mx - o.cx, my - o.cy)
            rad = math.radians(o.angle)
            cos_a, sin_a = math.cos(rad), math.sin(rad)
            corners = {
                "tl": (-o.w/2, -o.h/2),
                "tr": ( o.w/2, -o.h/2),
                "bl": (-o.w/2,  o.h/2),
                "br": ( o.w/2,  o.h/2),
            }
            lx, ly = corners[self.drag_mode]
            orig_dist = math.hypot(lx, ly)
            if orig_dist > 0:
                scale = dist_now / orig_dist
                s.w = max(10, int(o.w * scale))
                s.h = max(10, int(o.h * scale))

    # ── Run ───────────────────────────────────────────────────────────────────

    def run(self):
        while True:
            for event in pygame.event.get():
                if not self.handle_event(event):
                    pygame.quit()
                    sys.exit()
            self.render()
            self.clock.tick(60)


if __name__ == "__main__":
    PaintApp().run()