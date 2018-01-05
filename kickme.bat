@echo off
setlocal
call activate twitter_bot

rem :: tweet test
rem python src/tweet.py secrets/kawa_bot.ini
rem :: get follower test
python src/get_follower_id.py secrets/kawa_bot.ini
rem :: get timeline test
python src/get_timeline.py secrets/kawa_bot.ini

call deactivate
endlocal

