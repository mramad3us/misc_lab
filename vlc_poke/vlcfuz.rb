#!/usr/bin/ruby

require "./spike.rb"

FuzzedFile.open("Flower_4.mp4","Fuzower_4.mp4",false) do |f|
    f.mutate(124,128924)
end
