import sys, pygame, resourceManager,client
pygame.init()
from gameObjects import MenuButton, TextField, TextObject

class Menu(object):
    def __init__(self,width,height):
        
        self.title_image,self.title_image_rect = resourceManager.load_image("title.png",-1)
        self.single_player = MenuButton.MenuButton("Singleplayer",(width/2,height-260),60)
        self.multi_player = MenuButton.MenuButton("Multiplayer",(width/2,height-180),60)

        self.server_text_field = TextField.TextField((width/2-150,height-230),14,35,"Server IP")
        self.username_text_field = TextField.TextField((width/2+150,height-230),10,35,"Your Name")
        
        self.connect_button = MenuButton.MenuButton("Connect",(width/2,height-180),60)

        self.error_message = TextObject.TextObject((width/2,height-100),35,(255,0,0),"")
        
    def update(self,program,events):

        if program.state == "MENU_Menu":
            self.single_player.update()
            self.multi_player.update()
            if self.single_player.is_clicked(events) == True:
                program.state = "SinglePlayer"
            if self.multi_player.is_clicked(events) == True:
                program.state = "MENU_MultiplayerLobby"
        elif program.state == "MENU_MultiplayerLobby":
            self.server_text_field.update(events)
            self.username_text_field.update(events)
            self.connect_button.update()
            if self.connect_button.is_clicked(events) == True:
                program.client.connect_to_server(self.error_message,self.server_text_field.message,self.username_text_field.message)
            
    def draw(self,program):
        
        if "MENU" in program.state:
            program.screen.blit(self.title_image,self.title_image_rect)
            self.error_message.draw(program.screen)

        if program.state == "MENU_Menu":
            self.single_player.draw(program.screen)
            self.multi_player.draw(program.screen)
        elif program.state == "MENU_MultiplayerLobby":
            self.server_text_field.draw(program.screen)
            self.username_text_field.draw(program.screen)
            self.connect_button.draw(program.screen)
        else:
            pass

class Program(object):
    def __init__(self):
        self.width = 800
        self.height = 500
        self.color = 0, 200, 0

        self.screen = pygame.display.set_mode((self.width,self.height))
        self.clock = pygame.time.Clock()
        self.state = "MENU_Menu"
        self.menu = Menu(self.width,self.height)
        self.client = client.Client()
    def update(self):

        listOfEvents = pygame.event.get()
        
        self.screen.fill(self.color)
        self.menu.update(self,listOfEvents)
        self.client.update(self.menu.error_message,listOfEvents)
        for event in listOfEvents:
            if event.type == pygame.QUIT:
                self.client.disconnect_from_server(self.menu.error_message)
                pygame.quit()
                sys.exit(1)
    def render(self):
        self.menu.draw(self)
        pygame.display.flip()
    def run(self):
        self.clock.tick(60)
        self.update()
        self.render()

if __name__ == "__main__":
    program = Program()
    while True:
        program.run()
    pygame.quit()
