from bgl import *
import VideoTexture as vt

from bgui.Widget import *

class Image(Widget):
	"""Widget for displaying images"""

	def __init__(self, parent, name, img, size=[0, 0], pos=[0, 0], options=BGUI_DEFUALT):
		"""The ImageWidget constructor

		Arguments:

		parent -- the widget's parent
		name -- the name of the widget
		img -- the image to use for the widget
		size -- a tuple containing the wdith and height
		pos -- a tuple containing the x and y position
		options -- various other options

		"""

		Widget.__init__(self, parent, name, size, pos, options)

		# Generate a texture
		id_buf = Buffer(GL_INT, 1)
		glGenTextures(1, id_buf)

		self.tex_id = id_buf.list[0]


		self.update_image(img)


	def update_image(self, img):
		"""Change's the image texture

		Arguments
		img -- the path to the new image

		"""

		glBindTexture(GL_TEXTURE_2D, self.tex_id)
		
		# Load the texture data
		image = vt.ImageFFmpeg(img)
		image.scale = False
		im_buf = image.image

		# Setup some parameters
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

		glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

		# Upload the texture data
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.size[0], image.size[1], 0,
						GL_RGBA, GL_UNSIGNED_BYTE, im_buf)

	def _draw(self):
		"""Draws the image"""
		
		# Enable textures
		glEnable(GL_TEXTURE_2D)

		# Bind the texture
		glBindTexture(GL_TEXTURE_2D, self.tex_id)
		texco = [(0, 0), (1, 0), (1, 1), (0, 1)]

		# Draw the textured quad
		glColor4f(1, 1, 1, 1)

		glBegin(GL_QUADS)
		for i in range(4):
			glTexCoord2f(texco[i][0], texco[i][1])
			glVertex2f(self.gl_position[i][0], self.gl_position[i][1])
		glEnd()

		glBindTexture(GL_TEXTURE_2D, 0)

		# Now draw the children
		Widget._draw(self)