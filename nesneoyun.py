import pygame
from sys import exit
from random import randint, choice
# Burada temel bir oyun objesi sinifi olusturuluyor. Bu sinif, Pygame'in Sprite sinifini miras alır.
class GameObject(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()  # Görsel yukleme
        self.rect = self.image.get_rect(midbottom=(x, y))  # Objenin dikdortgeni, belirli bir pozisyona gelecek sekilde ayarlaniyor.
# Alt siniflar icin update metodu
    def update(self):
        pass  
# GameObject sinifindan turetilen oyuncu sinifi
class Player(GameObject):
    def __init__(self):
        super().__init__('graphics/kedi.png', 80, 300) 
        self.gravity = 0  # Yerçekimi basta sifir
    # Oyuncunun tus girisleri
    def player_input(self):
        keys = pygame.key.get_pressed() 
        # Oyuncu yere temas ediyorsa zıplamasına izin verilir.
    # Ziplama sirasinda yukari dogru bir kuvvet uygulanır.
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:  
            self.gravity = -20  
    # Yercekimi uygulanmasi
    def apply_gravity(self):
        self.gravity += 1  # Yercekimi her frame'de bir 1 artar
        self.rect.y += self.gravity  # Oyuncunun y konumu guncellenir.
        if self.rect.bottom >= 300:  # Oyuncu zeminin altina inme durumunda zemine sabitlenir.
            self.rect.bottom = 300
    # Oyuncu hareketlerini guncelleme
    def update(self):
        self.player_input()  # Tus girislerini kontrol eder
        self.apply_gravity()  # Yerçekimi uygulanır.
# GameObject sinifindan turetilen Engel sinifi
class Obstacle(GameObject):
    def __init__(_self, type):
        # Engel turune gore objenin degerleri degisir
        if type == 'kus': 
            image_path = 'graphics/kus.png'
            y_pos = 210
        elif type == 'kaya':
            image_path = 'graphics/tas.png'
            y_pos = 300
        super().__init__(image_path, randint(900, 1100), y_pos)  # Engel ekranın saginda rastgele bir x pozisyonunda oluşturulur

    # Engeli sola dogru hareket ettirir ve yok eder
    def update(self):
        self.rect.x -= 6  
        self.destroy()  # Ekran disina ciktiysa yok edilir
    
    # Engel ekranin solundan ciktiysa hafizadan silinir
    def destroy(self):
        if self.rect.x <= -100: 
            self.kill()  # Pygame'in kill() metodu ile Sprite yok edilir

# Skorun ekranda gosterilme kismi
def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time  # Oyun suresi hesaplanmasi
    # Skor yazdirma
    score_surf = game_font.render(f'Score: {current_time}', False, (255, 255, 255))  
    score_rect = score_surf.get_rect(center=(400, 50)) 
    screen.blit(score_surf, score_rect) 
    # Skor degeri dondurulur
    return current_time  

# Oyuncunun engellerle carpisma kontrolu kismi
def collision_sprite():
    # Carpisma var ise oyun durumu False olarak dondurulur
    # Carpisma yoksa oyun durumu True olarak dondurulur
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):  
        return False  
    else:
        return True  

# Pygame baslatilmasi ve ekran ayarlari
pygame.init()
screen = pygame.display.set_mode((800, 400))  
pygame.display.set_caption('Dila Kurnaz')  
clock = pygame.time.Clock() 
# Oyunun fontu
game_font = pygame.font.Font(None, 50)
start_time = int(pygame.time.get_ticks() / 1000) 
game_active = True 
score = 0 

# Oyuncu ve engel icin SpriteGroup
player = pygame.sprite.GroupSingle()  
# Oyuncu nesnesi olusturulur
player.add(Player())
obstacle_group = pygame.sprite.Group()

# Arkaplan ve zemin görselleri yuklenir
sky_surface = pygame.image.load('graphics/background.gif').convert()
ground_surface = pygame.image.load('graphics/ground2.png').convert()

# Engel ekleme olayını belirli araliklarla tetiklemek için bir sayac tanimlanir
obstacle_timer = pygame.USEREVENT + 1  # Yeni bir özel Pygame olayı oluşturulur.
pygame.time.set_timer(obstacle_timer, 1500)  # 1500 milisaniyede bir bu olay tetiklenir.

# Oyun dongusu
while True:
    # Kullanici olaylarini kontrol eder
    for event in pygame.event.get():  
        # Cikis istegi kontrol edilir
        if event.type == pygame.QUIT:  
            pygame.quit()
            exit()

        # Oyun aktif ise ve engel olusturma event’i tetiklenmis ise engel olusturulur
        if game_active:
            if event.type == obstacle_timer: 
                # engel nesnesi olusturma
                obstacle_group.add(Obstacle(choice(['kus', 'kaya', 'kaya', 'kus', 'kaya'])))

    # Oyun aktifse yapilacak cizimler
    if game_active:
        screen.blit(sky_surface, (0, 0))  
        screen.blit(ground_surface, (0, 300)) 
        score = display_score()

        player.draw(screen) 
        player.update() 

        obstacle_group.draw(screen) 
        obstacle_group.update()  

        game_active = collision_sprite()
    
    # Oyun aktif degilse yapilacak cizimler (oyun bitis ekrani)
    else:
        
        screen.fill((0, 0, 0))  
        game_over_text = game_font.render("YOU'RE DEAD!", False, (255, 255, 255)) 
        game_over_rect = game_over_text.get_rect(center=(400, 200)) 
        screen.blit(game_over_text, game_over_rect)

        score_text = game_font.render(f'Final Score: {score}', False, (255, 255, 255))
        score_rect = score_text.get_rect(center=(400, 250))
        screen.blit(score_text, score_rect) 

    pygame.display.update()
    clock.tick(60)