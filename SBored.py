import app
import gui

import threading


app = app.App()
app.load()

##t = threading.Thread(target=app.k.start)
##t.start()




gui = gui.GUI(app)

gui.root.mainloop()


app.quit()
app.stop()

quit()
