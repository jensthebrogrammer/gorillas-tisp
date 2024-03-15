# gorillas-tisp
this is a classic gorilla game made in pygame. please leave suggestions if you have any ideas on how to improve the design.


how to set it up:

in order for this program to work you will need to download the pygame library. more information on how to download here https://pypi.org/project/pygame/
the game runs on 3 different files : the main file, the BLL (bussinis logic layer) and the PL (presentation layer).
it also needs some png files and txt files to work. these will be provided in the repository.



how it works:

when you start playing the game will ask for your names, after this the game will start. the first player will be asked to type in an angle.
to confirm your input press space. if you accidently type someting wrong, you can try again by pressing delete (backspace will not work).
then the first player will give in a speed. the gorilla will trow a banana at the given angle and speed. then player2 has to do the same.
you dont have to worry about the dirrection, the program takes care of that itself. if a gorilla is hit, it will lose one life and the circomstances will change.
so you can't just give in the same values in a feww times and win. when you take all of the other players life, you win.




the settings file:

you will find a settings file in the repository. this file can be used to change certain messures of the game. for example: you could add extra lives to your karakter or make it bigger.
!!! be carefull wich settings you alter. this file isn't fully tested yet.
