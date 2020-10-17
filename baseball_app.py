#!/usr/bin/python3

import tkinter as tk
import pybaseball
from PIL import ImageTk, Image
import pandas as pd

HEIGHT = 1000
WIDTH = 1400

# Get splits and print them to the screen
def get_splits(splits, player):

    df = pd.DataFrame(splits, dtype=object)
    # dfStyler = df.style.set_properties(**{'text-align': 'left'})
    # dfStyler.set_table_styles([dict(selector='th', props=[('text-align', 'left')])])

    txt_box.config(state='normal')
    txt_box.delete('1.0', 'end')
    txt_box.insert(tk.END, f'LOADING...\n\n\n', "bold")
    txt_box.insert(tk.END, player.upper() + '\n\n\n', "bold")
    # df = tabulate.tabulate(df.style.dataframe(df), headers='keys', tablefmt='psql')

    txt_box.insert(tk.END, df)
    txt_box.config(state='disabled')

# Write the data to an excel file using pandas dataframe's 
def write_splits_to_excel(bref_id, player, mlbam):
    with pd.ExcelWriter(f'{player}.xlsx') as writer:
        for year in [2020, 2019, 2018, 2017]:
            try:
                lookup = pybaseball.get_splits(str(bref_id), year=year, pitching_splits=True)
            except:
                lookup = pybaseball.get_splits(str(bref_id), year=year)
        
            try:
                df = pd.DataFrame(lookup, dtype=object)
                df.to_excel(writer, sheet_name=f'{year} Splits')

            except:
                pass
        
        try:
            stats = pybaseball.statcast_batter('2020-04-01', '2020-10-25', player_id=int(mlbam))
        except:
            stats = pybaseball.statcast_pitcher('2020-04-1', '2020-10-25', player_id=int(mlbam))

        try:
            df = pd.DataFrame(stats)
            df.to_excel(writer, sheet_name='Statcast')
        except:
            pass
            
        for another_year in [2020, 2019, 2018, 2017]:
            exit_velo = pybaseball.statcast_batter_exitvelo_barrels(year=another_year)
            df = pd.DataFrame(exit_velo)
            df.to_excel(writer, sheet_name=f'{another_year} EV')

    print('Finished writing data')

# Function grabs player ID and fetches splits 
def get_player_id(player):

    data = player.lower().split()
    data = pybaseball.playerid_lookup(data[1], data[0])
    bref = data['key_bbref'][0]

    try:
        lookup = pybaseball.get_splits(str(bref), year=2020, pitching_splits=True)

    except:
        lookup = pybaseball.get_splits(str(bref), year=2020)

    pd.set_option('display.expand_frame_repr', False)
    pd.options.display.max_rows = None

    mlbam = data['key_mlbam'][0]
    get_splits(lookup, player)

    print('Writing data to an Excel file...')
    write_splits_to_excel(bref, player, mlbam)

root = tk.Tk()

# Create a canvas (can place graphics, text, widgets or frames on it)
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

# Grab the image in the folder and attach it to the root background
background_image = ImageTk.PhotoImage(Image.open('Wrigley-Field.png'))
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

# Create a frame for the upper button and entry box
frame = tk.Frame(root, bg='#0377fc', bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=.85, relheight=0.1, anchor='n')

# Create the entry box to the left of where the button will be 
entry = tk.Entry(frame, font=('Fira Code', 15))
entry.place(relwidth=0.65, relheight=1)

# Create the button to the right of the entry box 
button = tk.Button(frame, text='Get Player', font=('Fira Code', 14), command=lambda: get_player_id(entry.get()))
button.place(relx=0.7, relwidth=0.3, relheight=1)

# Create the lower frame for the stats to be printed 
lower_frame = tk.Frame(root, bg='#0377fc', bd=10)
lower_frame.place(relx=0.5, rely=0.25, relwidth=.85, relheight=0.6, anchor='n')

# Create scrollbar if the stats are too long 
my_scrollbar = tk.Scrollbar(lower_frame, orient='vertical')
my_scrollbar.pack(side='right', fill='y')

# Create the text box that will hold the scraped data 
txt_box = tk.Text(lower_frame,font=('Modern', 8), bd=4, yscrollcommand=my_scrollbar.set)
txt_box.tag_configure("bold", font="Modern 8 bold")
txt_box.pack(expand=1, fill='both')

# Attach scrollbar to text box 
my_scrollbar.config(command=txt_box.yview)
txt_box.config(state='disabled')
root.mainloop()



