MonthValue=$((60*60*24*30))
DateUnix=$( date '+%s' )
Total=$(($DateUnix-$MonthValue))
FileNametx=$( date '+%d-%m-%Y' )
EndPoint=https://z3nadvocate314.zendesk.com/api/v2/incremental/users.json?start_time=
curl $EndPoint$Total \
  -v -u xxxx:**** > /private/tmp/$FileNametx-Users.txt
