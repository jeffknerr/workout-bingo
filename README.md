# workout-bingo
silly bingo game to get ready for skiing

# todo

- check that all current_workouts are the same (not +1 or -1)
- change procmai recipe to also save a copy to aaa.bingo
- something to determine game over/winner
- where to put the rsyncs for updated boards?
- take all cs.swat.edu specific stuff outside of code/git
- fix up this readme :)
- set up cron to call bingoemail.py program
- full game test with test emails
- full game test with beta tester emails
- launch on Dec 1

# outline

- add email addresses, one per line, to `.emails` file
- run newgame.py to create new game files and directories
    - creates dir and card.txt file for each user
    - calls makecard.py on card.txt file
    - creates .done file
    - should also send out "new game" email??? or let cron do that??
- set up procmail entry to look for [JK Bingo] Subject lines
    - save to location?
    - call script on email file
    - update ".done" file???
    - check for game over/winner??
- set up cron job to call pickworkout.py every T/Th/S
    - picks a random workout
    - sends an email to each player with workout, url, funny quote, leader board??
    - updates all .done files

- where do all of these games and cards go? need URLs!
- run all on CS, then rsync the entire dir to GDE??

# add emails
Add email addresses, one per line, to `.emails` file.

# add mark to image

Using the following font and point size, it appears the
"center" of the top right square is `x=60` and `y=130`.
So the first `convert` command below (from imagemagick) is for the
top left square, then next down one, down two, down two over one,
and finally down two (530) over two (460).

```
convert -font helvetica -fill blue -pointsize 100 -draw "text 60,130 'O'" card1.png output.png
convert -font helvetica -fill blue -pointsize 100 -draw "text 60,330 'O'" card1.png output.png
convert -font helvetica -fill blue -pointsize 100 -draw "text 60,530 'O'" card1.png output.png
convert -font helvetica -fill blue -pointsize 100 -draw "text 260,530 'O'" card1.png output.png
convert -font helvetica -fill blue -pointsize 100 -draw "text 460,530 'O'" card1.png output.png
```
