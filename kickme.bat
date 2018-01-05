@echo off
setlocal
call activate twitter_bot
python src/tweet.py secrets/kawa_bot.ini
call deactivate

endlocal

