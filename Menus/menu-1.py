#!/usr/bin/env python
import kalipi
from kalipi import *


#############################
## Global display settings ##

#++++++++++++++++++++++++++++#
#+   Select color scheme    +#

# Tron theme orange
##tron_regular = tron_ora
##tron_light = tron_yel
##tron_inverse = tron_whi

# Tron theme blue
tron_regular = tron_blu
tron_light = tron_whi
tron_inverse = tron_yel

#+           End            +#
#++++++++++++++++++++++++++++#

# Outer Border
pygame.draw.rect(screen, tron_light, (0,0,screen_x,screen_y),10)

## Global display settings ##
#############################

#############################
##    Local Functions      ##


# Check VNC status
def check_vnc():
    if 'vnc :1' in commands.getoutput('/bin/ps -ef'):
        return True
    else:
        return False


##    Local Functions      ##
#############################


#############################
##        Buttons          ##

# define all of the buttons
titleButton = Button(" " + kalipi.get_hostname() + "    " + kalipi.get_ip(), originX, originX, buttonHeight, buttonWidth * 3 + spacing * 2, tron_inverse, titleFont)
button1 = Button(labelPadding * " " + "       Exit", originX, originY, buttonHeight, buttonWidth, tron_light, labelFont)
button2 = Button(labelPadding * " " + "  X on TFT", originX + buttonWidth + spacing, originY, buttonHeight, buttonWidth, tron_light, labelFont)
button3 = Button(labelPadding * " " + " X on HDMI", originX + (buttonWidth * 2) + (spacing * 2), originY, buttonHeight, buttonWidth, tron_light, labelFont)
button4 = Button(labelPadding * " " + "  Shutdown", originX, originY + buttonHeight + spacing, buttonHeight, buttonWidth, tron_light, labelFont)
button5 = Button(labelPadding * " " + "VNC Server", originX + buttonWidth + spacing, originY + buttonHeight + spacing, buttonHeight, buttonWidth, tron_light, labelFont)
button6 = Button(labelPadding * " " + "  Terminal", originX + (buttonWidth * 2) + (spacing * 2), originY + buttonHeight + spacing, buttonHeight, buttonWidth, tron_light, labelFont)
button7 = Button(labelPadding * " " + "    Reboot", originX, originY + (buttonHeight * 2) + (spacing * 2), buttonHeight, buttonWidth, tron_light, labelFont)
button8 = Button(labelPadding * " " + " Screen Off", originX + buttonWidth + spacing, originY + (buttonHeight * 2) + (spacing * 2), buttonHeight, buttonWidth, tron_light, labelFont)
button9 = Button(labelPadding * " " + "      >>>", originX + (buttonWidth * 2) + (spacing * 2), originY + (buttonHeight * 2) + (spacing * 2), buttonHeight, buttonWidth, tron_light, labelFont)


def make_button(button):
    pygame.draw.rect(screen, tron_regular, (button.xpo-10,button.ypo-10,button.width,button.height),3)
    pygame.draw.rect(screen, tron_light, (button.xpo-9,button.ypo-9,button.width-1,button.height-1),1)
    pygame.draw.rect(screen, tron_regular, (button.xpo-8,button.ypo-8,button.width-2,button.height-2),1)
    font=pygame.font.Font(None,button.fntSize)
    label=font.render(str(button.text), 1, (button.color))
    screen.blit(label,(button.xpo,button.ypo+7))

# Define each button press action
def button(number):

    if number == 1:
        # Exit
        process = subprocess.call("setterm -term linux -back default -fore white -clear all", shell=True)
        pygame.quit()
        sys.exit()

    if number == 2:
	# X TFT
        pygame.quit()
        ## Requires "Anybody" in dpkg-reconfigure x11-common if we have scrolled pages previously
        ## kalipi.run_cmd("/usr/bin/sudo -u pi FRAMEBUFFER=/dev/fb1 startx")
        kalipi.run_cmd("/usr/bin/sudo FRAMEBUFFER=/dev/fb1 startx")
        os.execv(__file__, sys.argv)

    if number == 3:
        # X HDMI
        pygame.quit()
        ## Requires "Anybody" in dpkg-reconfigure x11-common if we have scrolled pages previously
        ## kalipi.run_cmd("/usr/bin/sudo -u pi FRAMEBUFFER=/dev/fb0 startx")
        kalipi.run_cmd("/usr/bin/sudo FRAMEBUFFER=/dev/fb0 startx")
        os.execv(__file__, sys.argv)

    if number == 4:
        # Shutdown
        pygame.quit()
        run_cmd("/usr/bin/sudo /sbin/shutdown -r now")
        sys.exit()

    if number == 5:
	# VNC
	if check_vnc():
		kalipi.run_cmd("/usr/bin/vncserver -kill :1")
		button4.color = tron_light
		make_button(button4)
		pygame.display.update()

	else:
		kalipi.run_cmd("/usr/bin/vncserver :1")
		button4.color = green
		make_button(button4)
		pygame.display.update()
	return

    if number == 6:
	# Terminal
        process = subprocess.call("setterm -term linux -back default -fore white -clear all", shell=True)
        pygame.quit()
        run_cmd("/usr/bin/sudo -u pi screen -RR")
        os.execv(__file__, sys.argv)

    if number == 7:
        # Reboot
        pygame.quit()
        run_cmd("/usr/bin/sudo /sbin/shutdown -r now")
        sys.exit()

    if number == 8:
        # Screen off
        pygame.quit()
        page=os.environ["MENUDIR"] + "menu_screenoff.py"
        os.execvp("python", ["python", page])
        sys.exit()

    if number == 9:
        # Next page
        pygame.quit()
        page=os.environ["MENUDIR"] + "menu-2.py"
        os.execvp("python", ["python", page])
        sys.exit()


# Buttons and labels
# See variables at the top of the document to adjust the menu

# Title
make_button(titleButton)

# First Row
# Button 1
button1.color = yellow
make_button(button1)

# Button 2
make_button(button2)

# Button 3
make_button(button3)


# Second Row
# Button 4
button4.color = yellow
make_button(button4)

# Button 5
if check_vnc():
	button5.color = green
	make_button(button5)
else:
	button5.color = tron_light
	make_button(button5)


# Button 6
make_button(button6)


# Third Row
# Button 7
button7.color = yellow
make_button(button7)

# Button 8
make_button(button8)

# Button 9
make_button(button9)

##        Buttons          ##
#############################


#############################
##        Input loop       ##

#While loop to manage touch screen inputs
while 1:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
            num = kalipi.on_touch()
            button(num)

        #ensure there is always a safe way to end the program if the touch screen fails
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
    pygame.display.update()
    ## Reduce CPU utilisation
    time.sleep(0.1)

##        Input loop       ##
#############################
