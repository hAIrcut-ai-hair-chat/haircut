from PIL import Image, ImageDraw

size = 200
img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

gray = '#757575'
dark_gray = '#5a5a5a'

body_x0, body_y0 = 60, 80
body_x1, body_y1 = 160, 120
draw.rounded_rectangle([body_x0, body_y0, body_x1, body_y1], radius=20, fill=gray)

nozzle_x0, nozzle_y0 = 155, 85
nozzle_x1, nozzle_y1 = 190, 115
draw.rounded_rectangle([nozzle_x0, nozzle_y0, nozzle_x1, nozzle_y1], radius=15, fill=gray)

draw.ellipse([185, 95, 195, 105], fill=dark_gray)

handle_x0, handle_y0 = 90, 115
handle_x1, handle_y1 = 115, 165
draw.rounded_rectangle([handle_x0, handle_y0, handle_x1, handle_y1], radius=10, fill=gray)

draw.line([102, 115, 102, 165], fill=dark_gray, width=3)

img.save('hair_dryer.png')
print("Imagem salva como 'hair_dryer.png'")