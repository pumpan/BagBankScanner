
DEFAULT_CHAT_FRAME:AddMessage("BagBankScanner |cff00FF00 loaded|cffffffff, /bbscan for options ")
BagBankScannerDB = BagBankScannerDB or { BagItems = {}, BankItems = {} }


local function ScanBags()
    BagBankScannerDB.BagItems = {} 
	--print("Scanning bags...")
	UIErrorsFrame:AddMessage("Scanning bags")
    for bag = 0, 4 do 
        for slot = 1, GetContainerNumSlots(bag) do
            local itemLink = GetContainerItemLink(bag, slot)
            local _, itemCount = GetContainerItemInfo(bag, slot)
            if itemLink then
                BagBankScannerDB.BagItems[itemLink] = (BagBankScannerDB.BagItems[itemLink] or 0) + itemCount
            end
        end
    end
end


local function ScanBank()
    if not BankFrame or not BankFrame:IsShown() then

        return
    end
	--print("Scanning bank...")
	UIErrorsFrame:AddMessage("Scanning bank")
    BagBankScannerDB.BankItems = {} 
    for bankID = 5, 11 do 
        for slot = 1, GetContainerNumSlots(bankID) do
            local itemLink = GetContainerItemLink(bankID, slot)
            local _, itemCount = GetContainerItemInfo(bankID, slot)
            if itemLink then
                BagBankScannerDB.BankItems[itemLink] = (BagBankScannerDB.BankItems[itemLink] or 0) + itemCount
            end
        end
    end
end


local function PrintMergedItemsContents()
    local mergedItems = {}

    for itemLink, itemCount in pairs(BagBankScannerDB.BagItems) do
        mergedItems[itemLink] = (mergedItems[itemLink] or 0) + itemCount
    end

    for itemLink, itemCount in pairs(BagBankScannerDB.BankItems) do
        mergedItems[itemLink] = (mergedItems[itemLink] or 0) + itemCount
    end

    for itemLink, itemCount in pairs(mergedItems) do
       -- print(itemLink .. ": " .. itemCount)
    end
end


local frame = CreateFrame("FRAME", "BagBankScannerFrame")
frame:RegisterEvent("BAG_UPDATE")
frame:RegisterEvent("PLAYERBANKSLOTS_CHANGED")
frame:SetScript("OnEvent", function()
    if event == "BAG_UPDATE" then
        ScanBags()
        ScanBank()		
    elseif event == "PLAYERBANKSLOTS_CHANGED" and BankFrame and BankFrame:IsShown() then
        ScanBank() 
    end
    PrintMergedItemsContents() 
end)


SLASH_BAGBANKSCANNER1 = '/bbscan'
SlashCmdList["BAGBANKSCANNER"] = function(msg)
    if msg == "bank" and BankFrame and BankFrame:IsShown() then
        ScanBank() 
        print("Bank contents scanned.")
    elseif msg == "bags" then
        ScanBags() 
        print("Bag contents scanned.")
    elseif msg == "all" then
        ScanBags() 
        if BankFrame and BankFrame:IsShown() then
            ScanBank() 
        end
        print("All contents scanned.")
    else
        print("Usage: /bbscan [bags|bank|all]. 'bank' option requires bank to be open.")
    end
    PrintMergedItemsContents() 
end
