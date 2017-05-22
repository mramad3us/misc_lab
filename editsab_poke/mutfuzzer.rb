#!/usr/bin/ruby

require "./spike.rb"

FuzzedFile.open("clean_2p.ets","Payloads/dirty_2p.ets",false) do |f|
    f.mutate(32,159,"charfill",'B')
end
