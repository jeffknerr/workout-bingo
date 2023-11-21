# workout-bingo
silly bingo game to get ready for skiing

# todo

x check that all current_workouts are the same (not +1 or -1)
x change procmail recipe to also save a copy to aaa.bingo
x something to determine game over/winner
x email all players when game is over
x write a utils.py file to pull all common functions into
x where to put the rsyncs for updated boards?
- take all cs.swat.edu specific stuff outside of code/git
- fix up this readme :) 
    x add cron entry
    x add procmail setup
x set up cron to call bingoemail.py program
x full game test with test emails
- full game test with beta tester emails
x .nogame file (cron checks if there's a game currently running)
- launch on Dec 1
x put index.html file in games dir
- assumes START/public_html exists


# outline

- add email addresses, one per line, to `.emails` file
- run newgame.py to create new game files and directories
    - creates dir and card.txt file for each user
    - calls makecard.py on card.txt file
    - creates .done file
    - cron job below sends email that game is going
    - removes .nogame file
- set up procmail entry to look for [JK Bingo] Subject lines
    - save to location?
    - call script on email file
    - update ".done" file???
    - check for game over/winner?? (if winner, create .nogame file)
- set up cron job to call bingoemail.py every T/Th/S
    - picks a random workout
    - updates .current_workout file
    - sends an email to each player with workout, url, funny quote, leader board??
    - updates all .done files

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

# cron entry

```
# bingo game at 8am, Tue/Thu/Sat
0 8 * * 2,4,6 python3 ~/repos/workout-bingo/bingoemail.py
```

# procmail entry

```
:0:
* ^Subject: Re: \[JK Bingo\] .*$
{
  :0 c
  aaa.IN.bingo

  :0
  | $HOME/repos/workout-bingo/processemail.py
}
```
