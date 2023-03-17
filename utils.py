from pythumb import Thumbnail
import pandas as pd
from PIL import Image, ImageDraw
import json


def save_youtube_thumbnail(youtube_link, path='data/thumbnails/'):
    t = Thumbnail(youtube_link)
    t.fetch()
    try:
        t.save(path)
    except:
        print('error saving thumbnail, path is either incorrect or image already exists')

        
def format_url(x):

    if not pd.isna(x):
        
        if 'youtu.be/' in x:
            ## check for format 'youtu.be'

            x = f"https://youtube.com/watch?v={x.split('youtu.be/')[-1]}"
            return x

        else:
            return x

    else:
        return None
    

def render_img_as_circle(input_path, output_folder_path='data/thumbnails_circle'):

    # Open the input image as numpy array, convert to RGB
    img=Image.open(input_path).convert("RGB")
    npImage=np.array(img)
    h,w=img.size

    ## make sure image is quadratic
    h=w

    # Create same size alpha layer with circle
    alpha = Image.new('L', img.size,0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice([0,0,h,w],0,360,fill=255)

    # Convert alpha Image to numpy array
    npAlpha=np.array(alpha)

    # Add alpha layer to RGB
    npImage=np.dstack((npImage,npAlpha))

    # Save with alpha
    Image.fromarray(npImage).save(f"{output_folder_path}/{input_path.split('/')[-1][:-4]}.png")


def load_json_geodata(json_file_path):

     with open(json_file_path, 'r') as j:
          geodata = json.loads(j.read())
     return geodata


def get_id_mapping_df_from_geodata(geodata):

    geo_list=[]

    for i in range(len(geodata['features'])):

        geo_list.append({
            'id': geodata['features'][i]['id'],  ## geo id
            'state_name': geodata['features'][i]['properties']['nam'],  ## state_name
            'district_name': geodata['features'][i]['properties']['laa']  ## district_name
        })
        
    return pd.DataFrame(geo_list)