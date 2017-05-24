#!/usr/bin/ruby

require "./spike.rb"

FuzzedFile.open("clean_2p.ets","Payloads/dirty_2p.ets",false) do |f|
    f.mutate(0x20,0x90-1,"charfill",'A')
    f.mutate(0x90,0x130-1,"charfill",'B')
    f.mutate(0x130,1026-1,"charfill",'C')
end
