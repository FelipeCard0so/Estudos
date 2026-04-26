import sys
import os
import locale
import datetime
import pygame

# ================= LOCALE =================
try:
    locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
except locale.Error:
    try:
        locale.setlocale(locale.LC_ALL, "Portuguese_Brazil.1252")
    except locale.Error:
        pass


class AirportClock:
    def __init__(self, mode="/s", hwnd=None):
        pygame.init()

        if mode == "/p" and hwnd:
            os.environ["SDL_VIDEODRIVER"] = "windib"
            os.environ["SDL_WINDOWID"] = str(hwnd)
            self.screen = pygame.display.set_mode((300, 200))
        else:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        self.width, self.height = self.screen.get_size()
        self.clock = pygame.time.Clock()
        self.running = True

        self.BG_COLOR = (9, 10, 10)
        self.FONT_COLOR = (250, 200, 5)

        # ================= FONTES =================
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.font_path = os.path.join(base_path, "fonts", "911porschav3.ttf")

        self.main_font_size = int(self.height * 0.35)
        self.date_font_size = int(self.height * 0.04)

        try:
            self.font_main = pygame.font.Font(self.font_path, self.main_font_size)
            self.font_date = pygame.font.Font(self.font_path, self.date_font_size)
        except Exception as e:
            print("Fonte não carregada:", e)
            self.font_main = pygame.font.SysFont("Arial Black", self.main_font_size)
            self.font_date = pygame.font.SysFont("Arial", self.date_font_size)

        self.last_mouse_pos = pygame.mouse.get_pos()

    @staticmethod
    def get_date_string():
        now = datetime.datetime.now()
        return now.strftime("%A, %d de %B de %Y").lower()

    def draw_glass_box(self, rect, radius):
        glass = pygame.Surface(rect.size, pygame.SRCALPHA)

        # Base vidro
        pygame.draw.rect(
            glass,
            (255, 255, 255, 35),
            glass.get_rect(),
            border_radius=radius,
        )

        # Highlight superior recortado
        highlight = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(
            highlight,
            (255, 255, 255, 25),
            (0, 0, rect.width, rect.height // 2),
            border_radius=radius,
        )

        glass.blit(highlight, (0, 0))

        # Borda sutil
        pygame.draw.rect(
            glass,
            (255, 255, 255, 90),
            glass.get_rect(),
            2,
            border_radius=radius,
        )

        self.screen.blit(glass, rect.topleft)

    def draw_time_boxes(self, hour, minute):
        padding = int(self.height * 0.05)
        spacing = int(self.width * 0.035)
        radius = int(self.height * 0.06)

        hour_surf = self.font_main.render(hour, True, self.FONT_COLOR)
        min_surf = self.font_main.render(minute, True, self.FONT_COLOR)

        box_height = hour_surf.get_height() + padding * 2
        box_width = max(hour_surf.get_width(), min_surf.get_width()) + padding * 2

        total_width = box_width * 2 + spacing
        start_x = (self.width - total_width) // 2
        center_y = self.height // 2

        hour_box = pygame.Rect(
            start_x, center_y - box_height // 2, box_width, box_height
        )
        min_box = pygame.Rect(
            start_x + box_width + spacing,
            center_y - box_height // 2,
            box_width,
            box_height,
        )

        self.draw_glass_box(hour_box, radius)
        self.draw_glass_box(min_box, radius)

        # Linha central split-flap
        pygame.draw.line(
            self.screen,
            (0, 0, 0),
            (hour_box.left + 12, center_y),
            (hour_box.right - 12, center_y),
            3,
        )
        pygame.draw.line(
            self.screen,
            (0, 0, 0),
            (min_box.left + 12, center_y),
            (min_box.right - 12, center_y),
            3,
        )

        self.screen.blit(hour_surf, hour_surf.get_rect(center=hour_box.center))
        self.screen.blit(min_surf, min_surf.get_rect(center=min_box.center))

    def run(self):
        pygame.mouse.set_visible(False)

        while self.running:
            self.screen.fill(self.BG_COLOR)

            now = datetime.datetime.now()
            self.draw_time_boxes(now.strftime("%H"), now.strftime("%M"))

            date_surf = self.font_date.render(
                self.get_date_string(), True, (170, 170, 170)
            )
            date_rect = date_surf.get_rect(
                bottomright=(self.width - 30, self.height - 20)
            )
            self.screen.blit(date_surf, date_rect)

            for event in pygame.event.get():
                if event.type in (
                    pygame.QUIT,
                    pygame.KEYDOWN,
                    pygame.MOUSEBUTTONDOWN,
                ):
                    self.running = False

                if event.type == pygame.MOUSEMOTION:
                    x, y = pygame.mouse.get_pos()
                    lx, ly = self.last_mouse_pos
                    if abs(x - lx) > 10 or abs(y - ly) > 10:
                        self.running = False

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()
        sys.exit()


# ================= ENTRY POINT =================
if __name__ == "__main__":
    mode = "/s"
    hwnd = None

    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()[:2]
        if mode == "/p" and len(sys.argv) > 2:
            hwnd = sys.argv[2]

    if mode == "/c":
        print("Configurações não implementadas.")
    else:
        app = AirportClock(mode, hwnd)
        app.run()
