from PIL import Image

# url
img = Image.open("testimg.jpg")
width, height = img.size

# slider from 1 to 350
slider = int(350)
scalew = int((width / 1000) * (slider))
scaleh = int((height / 1000) * (slider))

# Resize smoothly down to scalew x scaleh pixels
imgSmall = img.resize((scalew, scaleh), resample=Image.BILINEAR)
# Scale back up using NEAREST to original size
result = imgSmall.resize(img.size, Image.NEAREST)

# Save on jpg or png
result.save('resulttest.png')
