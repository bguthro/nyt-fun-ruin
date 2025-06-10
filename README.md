# NYT Games Fun Ruiner

This is the result of a joke that got out of hand.

It will solve some of the NYT games, and use iMessage to send it to whomever you don't like.

## Why would I want this?

Petty revenge?

Maybe you just don't enjoy fun. I'm not here to judge.

## How does this work?

This relies on you logging into NYT via your browser at least once. It then uses the cookie from that session to go look up solutions for:

- The daily mini
- Wordle
- Connections
- Spelling bee

Optionally, it can also send these results via iMessage (OSX required for this)

## Setup

A Makefile is provided to set up a python virtual environment.
Running `make` will set this up.

Alternately, you can manage this yourself, with `pip` - a `requirements.txt` file is provided.

## Usage & Examples

The most up-to-date program usage can always be found with the `--help` cmdline arg.

```
% ./nyt-fun-ruin.py --help
usage: nyt-fun-ruin.py [-h] [--date DATE] [--games GAMES] [--recipient RECIPIENT] [--wait]

options:
  -h, --help            show this help message and exit
  --date DATE, -d DATE  Date in YYYY-MM-DD format (default: today)
  --games GAMES, -g GAMES
                        Games to ruin (default: all). Options: mini, wordle, connections, spelling-bee, all
  --recipient RECIPIENT, -r RECIPIENT
                        iMessage recipient
  --wait, -w            Wait for the game to be available (default: False)
  ```

### Simple use case
Get the solutions for all of today's games, and just print the results.

*NOTE* - In these examples, I used an old date of "2024-05-26" for "today"

I only provide the example results for the first use case

```
% ./nyt-fun-ruin.py
Ruining fun...please wait.
---------------------------
Mini solution for 2024-05-26:
🅂 🄰 🄶 🄴 □
🄿 🄻 🄰 🄽 🅃
🄴 🄻 🅄 🄳 🄴
🅆 🄸 🅉 🄴 🄽
🅂 🄴 🄴 🄳 🅂

---------------------------
Wordle solution for 2024-05-26:
BEVEL

---------------------------
Connections solution for 2024-05-26:
FOUND ON A STOVE TOP:
   GRIDDLE,KETTLE,PAN,POT
ORNAMENTAL BORDER:
   FRILL,FRINGE,RUFFLE,TRIM
DEPOSIT, WITH “DOWN”:
   LAY,PLACE,PUT,SET
WORDS THAT SOUND LIKE PLURAL LETTERS:
   GEEZ,SEIZE,TEASE,WISE

---------------------------
Spelling bee words for 2024-05-26:
ABACI
ABACK
ACACIA
ACAI
ALACK
BACILLI
BACK
BECK
BIBLICAL
BLACK
BLACKBALL
CABAL
CABALA
CABBIE
CABLE
CACKLE
CAKE
CALL
CALLA
CALLABLE
CALLBACK
CELEB
CELIAC
CELL
CELLI
CILIA
CLACK
CLICK
CLICKABLE
ICICLE
ILIAC
KICK
KICKBACK
KICKBALL
LACE
LACK
LAIC
LAICAL
LICE
LICK
LILAC
```

## Just get the daily mini results
```
% ./nyt-fun-ruin.py --games mini
```

## Get all games, except for the spelling bee
```
% ./nyt-fun-ruin.py --games mini,wordle,connections
```

## Get all games for a different date
```
% ./nyt-fun-ruin.py --date 2024-05-27
```

## Get all games, and send results to an iMessage recipient with phone number 1234567890
```
% ./nyt-fun-ruin.py --recipient 1234567890
```

## Wait up to 24h for the games of a particular date to be published (usually tomorrow), and send results to a recipient
```
% ./nyt-fun-ruin.py --date 2024-05-28 --recipient 1234567890 --wait
```

## Wait up to 24h for just the mini game to be published, and send results to a recipient
```
% ./nyt-fun-ruin.py --date 2024-05-28 --games mini --recipient 1234567890 --wait
```