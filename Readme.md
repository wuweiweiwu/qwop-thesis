#Zookeeper bot

This is a python bot for the facebook messenger game Zookeeper. Very similar to Candy Crush

Here is a general gist of the program.

1. Screen grab
2. figure out whats in each cell
3. brute force the array and find swaps that will create 3 or 4 or 5 in a rows
4. simulate mouse clicks in those cells
5. repeat

I used support vector machines to predict what animal is in each square. I trained the machine using the pictures in the `training-images` folder.

I represented each picture as a 1 dimensional array of all of its rgb values `[r,g,b,r,g,b,r,g,b,r,g,b,r,g,b,r,g,b,r,g,b,....]` and that is how the support vector machine compares the input to the training images

Since calling `svc.fit` is very computationally expensive I cached the data in `trained.dat`

Since Candy Crush has been shown to be NP-hard, I brute forced the grid.
