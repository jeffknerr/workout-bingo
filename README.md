# workout-bingo
silly bingo game to get ready for skiing

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
