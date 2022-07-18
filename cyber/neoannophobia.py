"""
This is my solution to a challenge from ImaginaryCTF 2022. The idea is to beat the computer at a game,
a race to December 31. In this game, two players take turns saying days of the year ("January 30", "July 5", ...)

The first player (the computer) may start with any day in the month of January, and on each turn a player may say
another date that either has the same month or the same day as the previous date. You can also only progress forward
in time, never backwards.

For example, this is a valid series of moves:

Player 1: January 1
Player 2: February 1
Player 1: February 9
Player 2: July 9
Player 1: July 14
Player 2: July 30
Player 1: December 30
Player 2: December 31

This is an illegal set of moves:

Player 1: January 1
Player 2: July 29 (not same day or month)
Player 1: July 1 (going backwards in time)

The objective of the game is simple: be the first player to say December 31.

The computer will choose its own moves, and will always go first. To get the flag, you must win against the computer
100 times in a row.


My write-up:

To beat the bot I had to devise a strategy and also think backwards. Firstly, if the computer starts
with "January 31", I can just send "December 31". On the other hand, if it started with "January 30", then I can send
"November 30". In fact, the computer will be forced to send "December 30" back to me on the next turn. So I could win
the game by sending "December 31" back on my turn.

The idea is to develop techniques to force the computer to lose.

However, we have only dealt with the cases of "January 31" and "January 30" as first moves. Well, in fact,
the strategy goes on like this: if the computer starts with "January 29", I have to send "October 29" back. Indeed,
his only return options are: "October 31" (he loses because I return "December 31"), "October 30" (he loses because I
return "November 30" and then "December 31" as seen before), "November 29" (same pattern as for the previous option),
or "December 29" (he loses because I just have to return "December 31").
So it's all about strategy and anticipation.

You can just go back in the calendar by doing "September 28", "August 27",..., "February 21", "January 20".
However, there is a problem. I can beat the computer on any day except "January 20". After some research I discovered
that the first player always wins if he starts with "January 20". Indeed, in order not to have the strategy backfire
I decide to send "February 20" anyway to analyse what the computer sends me. I thought it would turn my own strategy
against me and return "February 21" and so on. But as it's a bot, and it's stupid, it didn't send back "February 21"
once, so I was able to resume my strategy quietly. After thinking about it, I think that the creator of the challenge
must have made the computer not follow the strategy, because otherwise it would have been simply impossible to beat it.

"""

from pwn import *

i = 1


def dec31_branch():  # function that wins if the month is December or if the day (before December) is 31
    conn.send(bytes("December 31\n", 'utf-8'))
    print("sent: December 31")
    bot_return = conn.recvline()
    print("end:", (" ".join((bot_return.decode().split())))[2:])
    if i == 100:
        bot_return = conn.recvline()
        print("FLAG:", " ".join((bot_return.decode().split())))
    else:
        bot_return = conn.recvline()
        bot_return = conn.recvline()
        bot_return = conn.recvline()


def nov30_branch():  # function that wins if the month is November or if the day (before November) is 30
    conn.send(bytes("November 30\n", 'utf-8'))
    print("sent: November 30")
    bot_return = conn.recvline()
    print("answer:", (" ".join((bot_return.decode().split())))[2:])
    dec31_branch()


def oct29_branch():  # function that wins if the month is October or if the day (before October) is 29
    conn.send(bytes("October 29\n", 'utf-8'))
    print("sent: October 29")
    bot_return = conn.recvline()
    print("answer:", (" ".join((bot_return.decode().split())))[2:])
    list_answer = bot_return.decode().split()
    if list_answer[2] == "31":
        dec31_branch()
    else:
        nov30_branch()


def sep28_branch():  # function that wins if the month is September or if the day (before September) is 28
    conn.send(bytes("September 28\n", 'utf-8'))
    print("sent: September 28")
    bot_return = conn.recvline()
    print("answer:", (" ".join((bot_return.decode().split())))[2:])
    list_answer = bot_return.decode().split()
    if (list_answer[1] == "September" and list_answer[2] == "29") or list_answer[1] == "October":
        oct29_branch()
    elif (list_answer[1] == "September" and list_answer[2] == "30") or list_answer[1] == "November":
        nov30_branch()
    elif list_answer[2] == "31" or list_answer[1] == "December":
        dec31_branch()


def aug27_branch():  # function that wins if the month is August or if the day (before August) is 27
    conn.send(bytes("August 27\n", 'utf-8'))
    print("sent: August 27")
    bot_return = conn.recvline()
    print("answer:", (" ".join((bot_return.decode().split())))[2:])
    list_answer = bot_return.decode().split()
    if (list_answer[1] == "August" and list_answer[2] == "28") or list_answer[1] == "September":
        sep28_branch()
    elif (list_answer[1] == "August" and list_answer[2] == "29") or list_answer[1] == "October":
        oct29_branch()
    elif list_answer[2] == "30" or list_answer[1] == "November":
        nov30_branch()
    elif list_answer[2] == "31" or list_answer[1] == "December":
        dec31_branch()


def jul26_branch():  # function that wins if the month is July or if the day (before July) is 26
    conn.send(bytes("July 26\n", 'utf-8'))
    print("sent: July 26")
    bot_return = conn.recvline()
    print("answer:", (" ".join((bot_return.decode().split())))[2:])
    list_answer = bot_return.decode().split()
    if (list_answer[1] == "July" and list_answer[2] == "27") or list_answer[1] == "August":
        aug27_branch()
    elif (list_answer[1] == "July" and list_answer[2] == "28") or list_answer[1] == "September":
        sep28_branch()
    elif (list_answer[1] == "July" and list_answer[2] == "29") or list_answer[1] == "October":
        oct29_branch()
    elif list_answer[2] == "30" or list_answer[1] == "November":
        nov30_branch()
    elif list_answer[2] == "31" or list_answer[1] == "December":
        dec31_branch()


def jun25_branch():  # function that wins if the month is June or if the day (before June) is 25
    conn.send(bytes("June 25\n", 'utf-8'))
    print("sent: June 25")
    bot_return = conn.recvline()
    print("answer:", (" ".join((bot_return.decode().split())))[2:])
    list_answer = bot_return.decode().split()
    if (list_answer[1] == "June" and list_answer[2] == "26") or list_answer[1] == "July":
        jul26_branch()
    elif (list_answer[1] == "June" and list_answer[2] == "27") or list_answer[1] == "August":
        aug27_branch()
    elif (list_answer[1] == "June" and list_answer[2] == "28") or list_answer[1] == "September":
        sep28_branch()
    elif (list_answer[1] == "June" and list_answer[2] == "29") or list_answer[1] == "October":
        oct29_branch()
    elif list_answer[2] == "30" or list_answer[1] == "November":
        nov30_branch()
    elif list_answer[2] == "31" or list_answer[1] == "December":
        dec31_branch()


def may24_branch():  # function that wins if the month is May or if the day (before May) is 24
    conn.send(bytes("May 24\n", 'utf-8'))
    print("sent: May 24")
    bot_return = conn.recvline()
    print("answer:", (" ".join((bot_return.decode().split())))[2:])
    list_answer = bot_return.decode().split()
    if (list_answer[1] == "May" and list_answer[2] == "25") or list_answer[1] == "June":
        jun25_branch()
    elif (list_answer[1] == "May" and list_answer[2] == "26") or list_answer[1] == "July":
        jul26_branch()
    elif (list_answer[1] == "May" and list_answer[2] == "27") or list_answer[1] == "August":
        aug27_branch()
    elif (list_answer[1] == "May" and list_answer[2] == "28") or list_answer[1] == "September":
        sep28_branch()
    elif (list_answer[1] == "May" and list_answer[2] == "29") or list_answer[1] == "October":
        oct29_branch()
    elif list_answer[2] == "30" or list_answer[1] == "November":
        nov30_branch()
    elif list_answer[2] == "31" or list_answer[1] == "December":
        dec31_branch()


def apr23_branch():  # function that wins if the month is April or if the day (before April) is 23
    conn.send(bytes("April 23\n", 'utf-8'))
    print("sent: April 23")
    bot_return = conn.recvline()
    print("answer:", (" ".join((bot_return.decode().split())))[2:])
    list_answer = bot_return.decode().split()
    if (list_answer[1] == "April" and list_answer[2] == "24") or list_answer[1] == "May":
        may24_branch()
    elif (list_answer[1] == "April" and list_answer[2] == "25") or list_answer[1] == "June":
        jun25_branch()
    elif (list_answer[1] == "April" and list_answer[2] == "26") or list_answer[1] == "July":
        jul26_branch()
    elif (list_answer[1] == "April" and list_answer[2] == "27") or list_answer[1] == "August":
        aug27_branch()
    elif (list_answer[1] == "April" and list_answer[2] == "28") or list_answer[1] == "September":
        sep28_branch()
    elif (list_answer[1] == "April" and list_answer[2] == "29") or list_answer[1] == "October":
        oct29_branch()
    elif list_answer[2] == "30" or list_answer[1] == "November":
        nov30_branch()
    elif list_answer[2] == "31" or list_answer[1] == "December":
        dec31_branch()


def mar22_branch():  # function that wins if the month is March or if the day (before March) is 22
    conn.send(bytes("March 22\n", 'utf-8'))
    print("sent: March 22")
    bot_return = conn.recvline()
    print("answer:", (" ".join((bot_return.decode().split())))[2:])
    list_answer = bot_return.decode().split()
    if (list_answer[1] == "March" and list_answer[2] == "23") or list_answer[1] == "April":
        apr23_branch()
    elif (list_answer[1] == "March" and list_answer[2] == "24") or list_answer[1] == "May":
        may24_branch()
    elif (list_answer[1] == "March" and list_answer[2] == "25") or list_answer[1] == "June":
        jun25_branch()
    elif (list_answer[1] == "March" and list_answer[2] == "26") or list_answer[1] == "July":
        jul26_branch()
    elif (list_answer[1] == "March" and list_answer[2] == "27") or list_answer[1] == "August":
        aug27_branch()
    elif (list_answer[1] == "March" and list_answer[2] == "28") or list_answer[1] == "September":
        sep28_branch()
    elif (list_answer[1] == "March" and list_answer[2] == "29") or list_answer[1] == "October":
        oct29_branch()
    elif list_answer[2] == "30" or list_answer[1] == "November":
        nov30_branch()
    elif list_answer[2] == "31" or list_answer[1] == "December":
        dec31_branch()


def feb21_branch():  # function that wins if the month is February or if the day (before February) is 21
    conn.send(bytes("February 21\n", 'utf-8'))
    print("sent: February 21")
    bot_return = conn.recvline()
    print("answer:", (" ".join((bot_return.decode().split())))[2:])
    list_answer = bot_return.decode().split()
    if (list_answer[1] == "February" and list_answer[2] == "22") or list_answer[1] == "March":
        mar22_branch()
    elif (list_answer[1] == "February" and list_answer[2] == "23") or list_answer[1] == "April":
        apr23_branch()
    elif (list_answer[1] == "February" and list_answer[2] == "24") or list_answer[1] == "May":
        may24_branch()
    elif (list_answer[1] == "February" and list_answer[2] == "25") or list_answer[1] == "June":
        jun25_branch()
    elif (list_answer[1] == "February" and list_answer[2] == "26") or list_answer[1] == "July":
        jul26_branch()
    elif (list_answer[1] == "February" and list_answer[2] == "27") or list_answer[1] == "August":
        aug27_branch()
    elif (list_answer[1] == "February" and list_answer[2] == "28") or list_answer[1] == "September":
        sep28_branch()
    elif (list_answer[1] == "February" and list_answer[2] == "29") or list_answer[1] == "October":
        oct29_branch()
    elif list_answer[2] == "30" or list_answer[1] == "November":
        nov30_branch()
    elif list_answer[2] == "31" or list_answer[1] == "December":
        dec31_branch()


def jan20_branch():  # function that wins if the month is January and if the day is before 20
    conn.send(bytes("January 20\n", 'utf-8'))
    print("sent: January 20")
    bot_return = conn.recvline()
    print("answer:", (" ".join((bot_return.decode().split())))[2:])
    list_answer = bot_return.decode().split()
    if (list_answer[1] == "January" and list_answer[2] == "21") or list_answer[1] == "February":
        feb21_branch()
    elif (list_answer[1] == "January" and list_answer[2] == "22") or list_answer[1] == "March":
        mar22_branch()
    elif (list_answer[1] == "January" and list_answer[2] == "23") or list_answer[1] == "April":
        apr23_branch()
    elif (list_answer[1] == "January" and list_answer[2] == "24") or list_answer[1] == "May":
        may24_branch()
    elif (list_answer[1] == "January" and list_answer[2] == "25") or list_answer[1] == "June":
        jun25_branch()
    elif (list_answer[1] == "January" and list_answer[2] == "26") or list_answer[1] == "July":
        jul26_branch()
    elif (list_answer[1] == "January" and list_answer[2] == "27") or list_answer[1] == "August":
        aug27_branch()
    elif (list_answer[1] == "January" and list_answer[2] == "28") or list_answer[1] == "September":
        sep28_branch()
    elif (list_answer[1] == "January" and list_answer[2] == "29") or list_answer[1] == "October":
        oct29_branch()
    elif list_answer[2] == "30" or list_answer[1] == "November":
        nov30_branch()
    elif list_answer[2] == "31" or list_answer[1] == "December":
        dec31_branch()


# there is very little chance that the computer will return "February 21" and if it does we only have to restart the
# program
def feb20_branch():  # function that handles the "January 20" problem
    conn.send(bytes("February 20\n", 'utf-8'))
    print("sent: February 20")
    bot_return = conn.recvline()
    print("answer:", (" ".join((bot_return.decode().split())))[2:])
    list_answer = bot_return.decode().split()
    if (list_answer[1] == "February" and list_answer[2] == "22") or list_answer[1] == "March":
        mar22_branch()
    elif (list_answer[1] == "February" and list_answer[2] == "23") or list_answer[1] == "April":
        apr23_branch()
    elif (list_answer[1] == "February" and list_answer[2] == "24") or list_answer[1] == "May":
        may24_branch()
    elif (list_answer[1] == "February" and list_answer[2] == "25") or list_answer[1] == "June":
        jun25_branch()
    elif (list_answer[1] == "February" and list_answer[2] == "26") or list_answer[1] == "July":
        jul26_branch()
    elif (list_answer[1] == "February" and list_answer[2] == "27") or list_answer[1] == "August":
        aug27_branch()
    elif (list_answer[1] == "February" and list_answer[2] == "28") or list_answer[1] == "September":
        sep28_branch()
    elif (list_answer[1] == "February" and list_answer[2] == "29") or list_answer[1] == "October":
        oct29_branch()
    elif list_answer[2] == "30" or list_answer[1] == "November":
        nov30_branch()
    elif list_answer[2] == "31" or list_answer[1] == "December":
        dec31_branch()


conn = remote('neoannophobia.chal.imaginaryctf.org', 1337)
conn.recvuntil(b'ROUND 1', drop=True)
bot_return = conn.recvline()
bot_return = conn.recvline()
while True:
    try:
        bot_return = conn.recvline()
        if i != 101:
            print("begin:", " ".join((bot_return.decode().split())))
        list_answer = bot_return.decode().split()
        if list_answer[1] == "31":
            dec31_branch()
        elif list_answer[1] == "30":
            nov30_branch()
        elif list_answer[1] == "29":
            oct29_branch()
        elif list_answer[1] == "28":
            sep28_branch()
        elif list_answer[1] == "27":
            aug27_branch()
        elif list_answer[1] == "26":
            jul26_branch()
        elif list_answer[1] == "25":
            jun25_branch()
        elif list_answer[1] == "24":
            may24_branch()
        elif list_answer[1] == "23":
            apr23_branch()
        elif list_answer[1] == "22":
            mar22_branch()
        elif list_answer[1] == "21":
            feb21_branch()
        elif list_answer[1] != "20":
            jan20_branch()
        elif list_answer[1] == "20":
            feb20_branch()

        print("row:", i)
        print("--------------------")
        i += 1
    except IndexError:
        conn.close()
        break
