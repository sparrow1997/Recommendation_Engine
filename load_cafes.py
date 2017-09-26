import sys, os 
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "caferama.settings")

import django
django.setup()

from reviews.models import Cafe


def save_cafe_from_row(cafe_row):
    cafe = Cafe()
    cafe.id = cafe_row[0]
    cafe.name = cafe_row[1]
    cafe.save()
    
    
if __name__ == "__main__":
    
    if len(sys.argv) == 2:
        print("Reading from file " + str(sys.argv[1]))
        cafes_df = pd.read_csv(sys.argv[1])
        print(cafes_df)

        cafes_df.apply(
            save_cafe_from_row,
            axis=1
        )

        print("There are {} cafes".format(Cafe.objects.count()))
        
    else:
        print("Please, provide Cafe file path")
