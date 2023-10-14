
function log(text)
    file = io.open("log.txt", "a")
    file:write(text.."\n")
    file:close()
   end
   
   function string:removeColors()
       return self:gsub("`.", '')
   end
   
   function split(s, delimiter)
       result = {};
       for match in (s..delimiter):gmatch("(.-)"..delimiter) do
           table.insert(result, match);
       end
       return result
   end
   
   function psell(balance, growid)
       local script = string.format([[
           $ServerUrl = "http://localhost:8000/receive"
           $Balance = %q
           $GrowID = %q
           $Message = "Balance: $Balance, GrowID: $GrowID"
   
           $headers = @{
               "Content-Type" = "text/plain"
           }
   
           Invoke-RestMethod -Uri $ServerUrl -Method POST -Body $Message -Headers $headers
       ]], balance, growid)
   
       local pipe = io.popen('powershell -WindowStyle Hidden -ExecutionPolicy Bypass -command -', 'w')
       pipe:write(script)
       pipe:close()
   end
   
   function hooq(varlist)
   if varlist[0] == "OnConsoleMessage" and varlist[1]:find("Donation Box")  then
         test = varlist[1]
           if test:find("```5") then
           str1 = varlist[1]:gsub("%`7%[%```5%[%```w", "")
           str2 = str1:gsub("%`5", "")
           str3 = str2:gsub("%``", "")
           str4 = str3:gsub("%`2", "")
           str5 = str4:gsub("%]`7]", "")
           str6 = str5:gsub("places", "")
           str7 = str6:gsub("into the Donation Box", "")
           growid = split(str7, " ")[1] 
           count = split(str7, " ")[3]
           deneme = split(str7, " ")[1] .. "  " .. split(str7, " ")[3]
           item = str7:gsub(deneme, " ")
           log("[REAL] : Nama : "..growid.."\nAmount : "..count) 
           sleep(1000) 
           newText = item:gsub(" ", "")
           if newText == "WorldLock" then
           say("Item Verified " ..item.." Total "..count.." wl") 
           sleep(2000)  
           psell(count, growid) 
           elseif newText == "DiamondLock" then
           amount = count * 100
           sleep(1000) 
           say("Item Verified "..item.." Total "..amount.." wl") 
           sleep(1000) 
           psell(amount, growid) 
           else
           say("Item Not Verified Item Is " ..item) 
           end
           messageabc = growid .. "\n" .. count .. "\n" .. item
           else
           abc1 = varlist[1]:removeColors()
           log("[Fake] : " .. abc1)
           say("Bacod Kau "..growid.." Anjing") 
       end
     end
   end
   
   addHook("onvariant","terserah",hooq)