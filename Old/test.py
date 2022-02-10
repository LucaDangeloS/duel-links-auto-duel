import pygetwindow as gw


window = gw.getWindowsWithTitle("Yu-Gi-Oh! DUEL LINKS")[0]

x = window.left
y = window.top
w = window.width
h = window.height

print("Window %s: \n" % window.title)
print("Location: (%d, %d)" % (x, y))
print("Size: (%d, %d)" % (w, h))
