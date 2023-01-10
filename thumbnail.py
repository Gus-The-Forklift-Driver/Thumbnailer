from PIL import Image
import os


def resizer(input: str, iterations, output_location: str = './', extention='jpg'):
    if iterations == 0:
        return
    source = Image.open(input)
    width, height = source.size
    filename = os.path.basename(input).split('.')[0]
    for x in range(iterations):
        new_height = int(height/2**(x+1))
        new_width = int(width/2**(x+1))
        if new_height <= 16:
            break
        source.thumbnail((new_width, new_height))
        # try:
        #     os.remove(f'{output_location}{filename}_{new_width}x{new_height}.{extention}')
        # except:
        #     pass
        print(f'saving to : {output_location}\{filename}_{new_width}x{new_height}.{extention}')
        try:
            source.save(f'{output_location}\{filename}_{new_width}x{new_height}.{extention}')
        except OSError:
            source = source.convert('RGB')
            source.save(f'{output_location}\{filename}_{new_width}x{new_height}.{extention}')
    return


#resizer('./test.jpg', 5)
