#!/usr/bin/ruby

require './spike'

def findit(lst,nm,f)
    #return the field f of the hash with "name"=nm from lst
    trim = lst.select{|h| h[:name]==nm}
    hsh = trim[0] if not trim.empty?
    return hsh[f]
end

def findval(lst,nm)
    #return the val field of the hash...
    return findit(lst,nm,:val)
end

SpikedFile.open("forged_2_0.ets","90") do |outf|

    magic = "27a41501"
    offsets = []
    offsets << {:name=>"magic_number",:val=>magic,:enc=>"H*",:off=>0}
    offsets << {:name=>"off_AD",:val=>0xAD,:enc=>"C",:off=>14}
    offsets << {:name=>"off_BD",:val=>0xBD,:enc=>"C",:off=>15}
    offsets << {:name=>"off_CD",:val=>0xCD,:enc=>"C",:off=>16}
    offsets << {:name=>"off_D4",:val=>0xD4,:enc=>"S",:off=>4}
    offsets << {:name=>"off_E1",:val=>0xE1,:enc=>"S",:off=>26}
    offsets << {:name=>"off_F1",:val=>0xF1,:enc=>"L",:off=>28}
    offsets << {:name=>"off_SZ",:val=>0x00,:enc=>"L",:off=>8}

    offsets.each do |offset|
        outf.insert(offset[:val],offset[:enc],offset[:off])
    end

    file_size = findval(offsets,"off_D4")*32 + 
                findval(offsets,"off_E1")*4  + 
                findval(offsets,"off_F1")    +
                findval(offsets,"off_SZ")

    #puts "Taget size : #{file_size}"
    footer_off = file_size - 1

    footer = {:name=>"footer",:val=>0x41,:enc=>"C",:off=>footer_off}
    outf.insert(footer[:val],footer[:enc],footer[:off])
end

