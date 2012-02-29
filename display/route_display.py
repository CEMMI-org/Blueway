from config import CONFIG, mapping, Ds
import os

if CONFIG.getMode() == "LIVE":
    print "LIVE Mode!"
    from display import *
    sockets = make_sockets(Ds)
    def route_displayi(data,CM=colormap.MATLAB_COLORMAP):
        imdisplayi(data,sockets,mapping,CM)
    def route_display(data):
        imdisplay(data,sockets,mapping)
else:
    if CONFIG.openbrowser:
        import webbrowser
    from sim_common import *    
    sockets = make_sockets(Ds);

    if CONFIG.getMode() == "WEB":
        print "WebSocket Mode"
        from web import web_server
        screen=web_server.WebScreen()
        if CONFIG.openbrowser: 
            webbrowser.open('http://localhost:8000/')
    if CONFIG.getMode() == "FILE":
        from file import sim_display
        screen=sim_display.FileScreen()
        print "File Mode"
        print "warning, file mode will be deprecated soon. Download pygame if websockets don't work for you"
        if CONFIG.openbrowser: 
            webbrowser.open(os.getcwd()+'/LEDs.html')
    if CONFIG.getMode() == "GAME":
        from game import pg_display
        screen=pg_display.GameScreen()
        print "PyGame Mode"

    locs = make_locs(sockets)
    screen.setup_screen([0,0,500,50],locs)

    
    def route_displayi(data,CM=colormap.MATLAB_COLORMAP):
        imdisplayi(data,sockets,mapping,screen,CM);

    def route_display(data):
        imdisplay(data,sockets,mapping,screen);

