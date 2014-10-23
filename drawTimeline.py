import pygame, sys
from pygame.locals import *
import loadData as ld

pygame.init()

TITLE = "Timeline"


width = int(1280)
height = int(720)

TIMEUNITWIDTH = 30
STARTTIME = 1830
LINESPACING = 10


# set up the colors
BLACK   = (  0,   0,   0)
GREY   =  (127, 127, 127)
WHITE   = (255, 255, 255)
RED     = (255,   0,   0)
ORANGE  = (255, 165,   0)
YELLOW  = (255, 255,   0)
YELLOWGREEN = (127, 155, 0)
GREEN   = (  0, 255,   0)
GREENCYAN = (0, 255, 127)
CYAN    = (  0, 255, 255)
AZURE   = (  0, 127, 255)
BLUE    = (  0,   0, 255)
VIOLET  = (127,   0, 255)
MAGENTA = (255,   0, 255)
ROSE    = (255,   0, 127)

BGCOLOR = WHITE

FONTSMALL = pygame.font.SysFont("Arial", 10)
FONTMEDIUM = pygame.font.SysFont("Arial", 20)
FONTLARGE = pygame.font.SysFont("Arial", 50)

DISPLAYSURF = pygame.display.set_mode((width, height), HWSURFACE|DOUBLEBUF|RESIZABLE)

gebiedenDict = {}
gebiedenNameDict = {}
cityDict = {}
cityList = []
provincieColors={"Groningen":RED,"Friesland":ORANGE,"Drenthe":YELLOW,"Overijssel":YELLOWGREEN,"Flevoland":GREEN,"Gelderland":GREENCYAN,"Utrecht":CYAN,"Noord-Holland":AZURE,"Zuid-Holland":BLUE,"Zeeland":VIOLET,"Noord-Brabant":MAGENTA,"Limburg":ROSE, "":GREY}
PROVINCIE = "all"

# set up key repeating so we can hold down the key to scroll.
old_k_delay, old_k_interval = pygame.key.get_repeat()
pygame.key.set_repeat (500, 30)

scrollPosition = [0,10]
scrollSpeed = TIMEUNITWIDTH
cityHeight = {}

pygame.display.set_caption(TITLE+" - "+PROVINCIE)


REORDER = USEREVENT + 1
orderDelay = 50
pygame.time.set_timer(REORDER, orderDelay)

def plot():
    drawList()
    startTick = pygame.time
    print startTick
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                closeWindow()
            elif event.type == pygame.VIDEORESIZE:
                updateScreenSize(event.size)
            elif event.type == REORDER:
                orderCityList()



            # scroll up
            if pygame.key.get_pressed()[pygame.K_UP] != 0:
                scrollPosition[1] = scrollPosition[1]+scrollSpeed
                #make sure we don't scroll to far up
                scrollPosition[1] = 10 if scrollPosition[1] > 10 else scrollPosition[1]

            # scroll down
            if pygame.key.get_pressed()[pygame.K_DOWN] != 0:
                scrollPosition[1] = scrollPosition[1]-scrollSpeed

            if pygame.key.get_pressed()[pygame.K_RIGHT] != 0:
                scrollPosition[0] = scrollPosition[0]-scrollSpeed

            if pygame.key.get_pressed()[pygame.K_LEFT] != 0:
                scrollPosition[0] = scrollPosition[0]+scrollSpeed
                scrollPosition[0] = 0 if scrollPosition[0] > 0 else scrollPosition[0]

        drawList()
        pygame.display.update()

def closeWindow():
    pygame.key.set_repeat (old_k_delay, old_k_interval)
    pygame.quit()
    sys.exit()

def drawDict():
    DISPLAYSURF.fill(BGCOLOR)
    drawYears()

    i=1
    for element in cityDict:
        if element in gebiedenDict:
            city = gebiedenDict[element]
            cityData = cityDict[element]
            if PROVINCIE == 'all' or city['provincie'] == PROVINCIE:
                color = provincieColors[city["provincie"]]
                begin, eind = getTimePeriod(city)
                height = cityHeight[element]
                for elem in cityData:
                    if type(cityData[elem]) is dict:
                        if "nameChange" in cityData[elem]:
                            height = cityHeight[cityData[elem]["nameChange"]]
                        if "changes" in cityData[elem]:
                            for change in cityData[elem]["changes"]:
                                drawLink(change[0], element, int(elem), color)

                drawTimeline(city['name'],begin,eind, height,color)
                i += 1

def drawList():
    DISPLAYSURF.fill(BGCOLOR)

    for city in cityList:
        if city.code in gebiedenDict:
            if PROVINCIE == 'all' or city.province == PROVINCIE:

                cityProperties = gebiedenDict[city.code]
                color = provincieColors[city.province]
                begin, eind = getTimePeriod(cityProperties)
                height = cityHeight[city.code]

                drawTimeline(city.name,begin,eind, height,color)

                for change in city.changeList:
                    drawLink(change.fromCode, city.code, int(change.year), color)
    drawYears()


def drawYears():
    pygame.draw.rect(DISPLAYSURF, WHITE,(0,height-30,width,30))
    pygame.draw.rect(DISPLAYSURF,BLACK,(0,height-30,width,30),1) 
    drawText(str((-scrollPosition[0]/TIMEUNITWIDTH)+STARTTIME), 0-scrollPosition[0], -scrollPosition[1]+height-25, BLACK, "medium")
    drawText(str(((-scrollPosition[0]+width)/TIMEUNITWIDTH)+STARTTIME), width-50-scrollPosition[0], -scrollPosition[1]+height-25, BLACK, "medium")
    drawText(str(((-scrollPosition[0]+(width/2))/TIMEUNITWIDTH)+STARTTIME), (width/2)-50-scrollPosition[0], -scrollPosition[1]+height-25, BLACK, "medium")


def drawTimeline(name, startTime, endTime, height, color):
    start = ( startTime - STARTTIME ) * TIMEUNITWIDTH
    end =( endTime - STARTTIME ) * TIMEUNITWIDTH
    drawLine(color, [start, height], [end, height] )
    drawText(name, start, height-11, BLACK, "small")

def drawLink(originatingCity, newCity, year, color):
    if originatingCity in cityHeight:
        y = ( year - STARTTIME )  * TIMEUNITWIDTH
        drawLine(color, [y, cityHeight[originatingCity]],[y+3,
            cityHeight[newCity]])



def drawLine(color, start, end):
    start[1] = start[1]+scrollPosition[1]
    start[0] = start[0]+scrollPosition[0]
    end[1] = end[1]+scrollPosition[1]
    end[0] = end[0]+scrollPosition[0]
    pygame.draw.line(DISPLAYSURF, color, start, end,3)
    pygame.draw.circle(DISPLAYSURF, color, end, 3)

def drawText(text, x, y, color, size="medium"):
    if size=="small":
        font = FONTSMALL
    elif size=="medium":
        font = FONTMEDIUM
    elif size=="large":
        font = FONTLARGE
    else:
        font = FONTMEDIUM


    label = font.render(text, 3, color)
    DISPLAYSURF.blit(label, (x+scrollPosition[0],y+scrollPosition[1]))

def getTimePeriod(city):
    begin = int(city['begin'][:4])
    eind = int(city['eind'][:4]) if len(city['eind']) else 2014
    return begin, eind

def setCityHeights():
    i = 0
    for city in cityDict:
        if city in gebiedenDict and (PROVINCIE == 'all' or gebiedenDict[city]['provincie'] == PROVINCIE):
            cityHeight[city]=i*LINESPACING
            i += 1

def setCityHeightsList():
    i = 0
    for city in cityList:
        if city.code in gebiedenDict and (PROVINCIE == 'all' or city.province == PROVINCIE):
            cityHeight[city.code]=i*LINESPACING
            i += 1

def orderCityList():
    global cityList
    cityLinks = []
    cityIndexDict = {}
    for i, city in enumerate(cityList):
        cityIndexDict[city.code] = i
        cityLinks.append((city.code, [])) 
        if (PROVINCIE == 'all' or city.province == PROVINCIE):
            for change in city.changeList:
                if not change.fromCode in cityLinks[-1][1]:
                    cityLinks[-1][1].append(change.fromCode)



    for links in cityLinks:
        if len(links[1]):
            cityIndex = cityIndexDict[links[0]]
            indexes = [cityIndex]
            for link in links[1]:
                if link in cityIndexDict:
                    linkIndex =cityIndexDict[link]
                    indexes.append(linkIndex)

            avg = float(sum(indexes))/len(indexes)
            for link in links[1]:
                if link in cityIndexDict:
                    linkIndex =cityIndexDict[link]
                    if cityIndex-avg>1:
                        tempCity = cityList[cityIndex-1]
                        cityList[cityIndex-1] = cityList[cityIndex]
                        cityList[cityIndex] = tempCity
                        cityIndexDict[links[0]] = cityIndex-1
                    elif cityIndex-avg < -1:
                        tempCity = cityList[cityIndex+1]
                        cityList[cityIndex+1] = cityList[cityIndex]
                        cityList[cityIndex] = tempCity
                        cityIndexDict[links[0]] = cityIndex+1

    setCityHeightsList()



# Updates the screen size and scales everything inside accordingly.
def updateScreenSize(size):
    global width, height
    width = size[0]
    height = size[1]

    DISPLAYSURF = pygame.display.set_mode((width,height), \
                                           HWSURFACE|DOUBLEBUF|RESIZABLE)



def init():
    global gebiedenDict, gebiedenNameDict, cityDict, cityList
    gebiedenDict, gebiedenNameDict = ld.loadGebieden()

    cityList = ld.loadDataListFromTXT("beschrijving.txt", gebiedenNameDict, gebiedenDict)

    cityList.sort(key=lambda x: x.province, reverse=True)
    # orderCityList()
    setCityHeightsList()
    plot()


init()