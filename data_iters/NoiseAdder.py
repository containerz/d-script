from PIL import Image, ImageOps, ImageMath, ImageEnhance

#%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
import glob

class NoiseAdder:

    @staticmethod
    def nmec_post(x, **kwargs):
        stainer = NoiseAdder()
        x = stainer.add_noise(Image.fromarray(x, 'L'), kwargs["shingle_dim"], kwargs["rng"])
        return x
    
    def __init__(self, noisedir):
        self.noisedir = noisedir
        imagenames = glob.glob(noisedir+'/*.*')
        self.images = [ Image.open(imname).convert('L') for imname in imagenames ]
        # self.stain = Image.open("/work/johnm/d-script/data_iters/coffee_stain_1.jpg").convert('RGBA')
    
    def add_noise(self, shingle_img, shingle_dim, rng):
        
        #assumes RGBA stain > shingle in both dim
        #assumes shingle is 'L'
        assert shingle_img is not None
        assert shingle_dim is not None
        assert rng is not None
        
        # Convert the image
        shingle_img = Image.fromarray( shingle_img, 'L')
        
        # Choose a random image and a random section inside of the image
        stain_img = self.images[ rng.randint( len(self.images), size=1 ) ]
        stain_w, stain_h = stain_img.size
        max_rand_x = stain_w - shingle_dim[1]
        max_rand_y = stain_h - shingle_dim[0]
        startx = rng.randint(max_rand_x)
        starty = rng.randint(max_rand_y)
        rand_cropped_stain = stain_img.crop((startx, starty, startx+shingle_dim[1], starty+shingle_dim[0]))
        rand_bright = rng.random_sample()+1.0
        
        # Invert both images and add them together
        rand_faded_stain = ImageEnhance.Brightness(rand_cropped_stain).enhance(rand_bright)
        stain_inv = ImageOps.invert(rand_faded_stain)
        shingle_inv = ImageOps.invert(shingle_img)
        
        assert stain_inv is not None
        assert shingle_inv is not None
        final_img = np.asarray(ImageOps.invert(ImageMath.eval("convert(a+b, 'L')", a=stain_inv, b=shingle_inv)))
        assert final_img is not None
        return final_img

