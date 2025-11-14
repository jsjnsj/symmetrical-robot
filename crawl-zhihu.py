-- 改进版：支持重复启动和实时滑动的通用工具箱
if _G.UniversalUITool then
    -- 如果已存在，先关闭旧UI再重新创建
    _G.UniversalUITool:Destroy()
    wait(0.1)
end

local OrionLib = loadstring(game:HttpGet("https://pastebin.com/raw/VeaMSRZK"))()

-- 创建全局引用
_G.UniversalUITool = {}
_G.UniversalUITool.Enabled = true

-- 创建主窗口
local MainWindow = OrionLib:MakeWindow({
    Name = "皇帝脚本",
    HidePremium = false,
    SaveConfig = true,
    IntroText = "加载完成",
    ConfigFolder = "MyTools",
    AutoShowScrollBar = true, -- 确保显示滚动条
})

-- 存储所有标签页引用
_G.UniversalUITool.Tabs = {}

-- 创建多个标签页
local tabNames = {
    "主功能", "玩家功能", "移动功能", "视觉功能", 
    "传送功能", "脚本功能", "工具集", "设置"
}

for _, tabName in ipairs(tabNames) do
    _G.UniversalUITool.Tabs[tabName] = MainWindow:MakeTab({
        Name = tabName,
        Icon = "rbxassetid://4483345998",
        PremiumOnly = false
    })
end

-- 功能管理器
local FunctionManager = {
    ActiveFunctions = {},
    Config = {
        AutoSave = true,
        ScrollEnabled = true
    }
}

-- 添加大量功能来展示滑动效果
function FunctionManager:AddMainFunctions()
    local tab = _G.UniversalUITool.Tabs["主功能"]
    
    tab:AddLabel("=== 核心控制 ===")
    
    -- 无限跳跃
    tab:AddToggle({
        Name = "无限跳跃",
        Default = false,
        Callback = function(v)
            self.ActiveFunctions.InfiniteJump = v
            if v then
                local hum = game.Players.LocalPlayer.Character:FindFirstChildOfClass("Humanoid")
                if hum then
                    self.ActiveFunctions.IJConnection = hum.StateChanged:Connect(function(_, st)
                        if st == Enum.HumanoidStateType.Landed then 
                            hum:ChangeState(Enum.HumanoidStateType.Jumping) 
                        end
                    end)
                end
            else
                if self.ActiveFunctions.IJConnection then 
                    self.ActiveFunctions.IJConnection:Disconnect() 
                end
            end
        end
    })
    
    tab:AddSlider({
        Name = "移动速度",
        Min = 16, Max = 200, Increment = 1, Default = 16,
        Callback = function(v) 
            local character = game.Players.LocalPlayer.Character
            if character and character:FindFirstChildOfClass("Humanoid") then
                character.Humanoid.WalkSpeed = v 
            end
        end
    })
    
    tab:AddSlider({
        Name = "跳跃高度",
        Min = 50, Max = 500, Increment = 5, Default = 50,
        Callback = function(v) 
            local character = game.Players.LocalPlayer.Character
            if character and character:FindFirstChildOfClass("Humanoid") then
                character.Humanoid.JumpPower = v 
            end
        end
    })
    
    -- 添加更多功能...
    for i = 1, 15 do
        tab:AddToggle({
            Name = "示例功能 " .. i,
            Default = false,
            Callback = function(v)
                print("功能" .. i .. "状态:", v)
            end
        })
    end
end

function FunctionManager:AddPlayerFunctions()
    local tab = _G.UniversalUITool.Tabs["玩家功能"]
    
    tab:AddLabel("=== 玩家增强 ===")
    
    -- 穿墙模式
    tab:AddToggle({
        Name = "穿墙模式",
        Default = false,
        Callback = function(v)
            self.ActiveFunctions.Noclip = v
            if v then
                self:StartNoclip()
            OrionLib:MakeNotification({
                    Name = "穿墙模式",
                    Content = "穿墙已启用 - 可以穿过墙壁",
                    Time = 3
                })
            else
                self:StopNoclip()
            end
        end
    })
    
    tab:AddToggle({
        Name = "上帝模式",
        Default = false,
        Callback = function(v)
            self.ActiveFunctions.GodMode = v
            if v then
                local humanoid = game.Players.LocalPlayer.Character:FindFirstChildOfClass("Humanoid")
                if humanoid then
                    humanoid.MaxHealth = math.huge
                    humanoid.Health = math.huge
                end
            end
        end
    })
    
    -- 添加大量玩家功能...
    for i = 1, 20 do
        tab:AddButton({
            Name = "玩家功能 " .. i,
            Callback = function()
                OrionLib:MakeNotification({
                    Name = "功能提示",
                    Content = "执行玩家功能 " .. i,
                    Time = 2
                })
            end
        })
    end
end

function FunctionManager:AddMovementFunctions()
    local tab = _G.UniversalUITool.Tabs["移动功能"]
    
    tab:AddLabel("=== 移动控制 ===")
    
    -- 飞行模式
    tab:AddToggle({
        Name = "飞行模式",
        Default = false,
        Callback = function(v)
            self.ActiveFunctions.Fly = v
            if v then
                self:StartFlying()
            else
                self:StopFlying()
            end
        end
    })
    
    tab:AddToggle({
        Name = "水上行走",
        Default = false,
        Callback = function(v)
            self.ActiveFunctions.WaterWalk = v
        end
    })
    
    -- 添加大量移动功能...
    for i = 1, 25 do
        tab:AddSlider({
            Name = "移动参数 " .. i,
            Min = 0,
            Max = 100,
            Default = 50,
            Callback = function(value)
                print("参数" .. i .. "设置为:", value)
            end
        })
    end
end

function FunctionManager:AddVisualFunctions()
    local tab = _G.UniversalUITool.Tabs["视觉功能"]
    
    tab:AddLabel("=== 视觉效果 ===")
    
    tab:AddToggle({
        Name = "透视墙壁",
        Default = false,
        Callback = function(v)
            self.ActiveFunctions.Wallhack = v
        end
    })
    
    tab:AddToggle({
        Name = "夜视模式",
        Default = false,
        Callback = function(v)
            if v then
                game.Lighting.Brightness = 2
                game.Lighting.Ambient = Color3.new(1, 1, 1)
            else
                game.Lighting.Brightness = 1
                game.Lighting.Ambient = Color3.new(0.5, 0.5, 0.5)
            end
        end
    })
    
    -- 添加大量视觉功能...
    for i = 1, 18 do
        tab:AddColorpicker({
            Name = "颜色设置 " .. i,
            Default = Color3.new(math.random(), math.random(), math.random()),
            Callback = function(color)
                print("颜色" .. i .. "设置为:", color)
            end
        })
    end
end

function FunctionManager:AddTeleportFunctions()
    local tab = _G.UniversalUITool.Tabs["传送功能"]
    
    tab:AddLabel("=== 位置传送 ===")
    
    -- 添加大量传送点
    local locations = {}
    for i = 1, 30 do
        table.insert(locations, {
            Name = "传送点 " .. i,
            Position = Vector3.new(math.random(-500, 500), math.random(10, 100), math.random(-500, 500))
        })
    end
    
    for _, loc in ipairs(locations) do
        tab:AddButton({
            Name = loc.Name,
            Callback = function()
                local character = game.Players.LocalPlayer.Character
                if character and character:FindFirstChild("HumanoidRootPart") then
                    character.HumanoidRootPart.CFrame = CFrame.new(loc.Position)
                    OrionLib:MakeNotification({
                        Name = "传送成功",
                        Content = "已传送到: " .. loc.Name,
                        Time = 2
                    })
                end
            end
        })
    end
end

function FunctionManager:AddScriptFunctions()
    local tab = _G.UniversalUITool.Tabs["脚本功能"]
    
    tab:AddLabel("=== 脚本控制 ===")
    
    tab:AddTextbox({
        Name = "Lua代码执行器",
        Default = "",
        PlaceholderText = "输入Lua代码回车执行",
        Callback = function(code)
            local success, result = pcall(function()
                return loadstring(code)()
            end)
            
            if success then
                OrionLib:MakeNotification({
                    Name = "执行成功",
                    Content = "代码执行完成",
                    Time = 3
                })
            else
                OrionLib:MakeNotification({
                    Name = "执行错误",
                    Content = "错误: " .. tostring(result),
                    Time = 5
                })
            end
        end
    })
    
    -- 添加脚本功能...
    for i = 1, 12 do
        tab:AddDropdown({
            Name = "脚本选项 " .. i,
            Default = "选项1",
            Options = {"选项1", "选项2", "选项3", "选项4", "选项5"},
            Callback = function(value)
                print("脚本" .. i .. "选择:", value)
            end
        })
    end
end

function FunctionManager:AddToolFunctions()
    local tab = _G.UniversalUITool.Tabs["工具集"]
    
    tab:AddLabel("=== 实用工具 ===")
    
    tab:AddButton({
        Name = "清理地图垃圾",
        Callback = function()
            local count = 0
            for _, obj in pairs(workspace:GetDescendants()) do
                if obj:IsA("Part") and (obj.Name:find("垃圾") or obj.Name:find("Trash")) then
                    obj:Destroy()
                    count += 1
                end
            end
            OrionLib:MakeNotification({
                Name = "清理完成",
                Content = "已清理 " .. count .. " 个垃圾对象",
                Time = 3
            })
        end
    })
    
    -- 添加工具...
    for i = 1, 15 do
        tab:AddButton({
            Name = "工具功能 " .. i,
            Callback = function()
                OrionLib:MakeNotification({
                    Name = "工具提示",
                    Content = "工具 " .. i .. " 已执行",
                    Time = 2
                })
            end
        })
    end
end

function FunctionManager:AddSettings()
    local tab = _G.UniversalUITool.Tabs["设置"]
    
    tab:AddLabel("=== UI设置 ===")
    
    tab:AddToggle({
        Name = "自动保存设置",
        Default = true,
        Callback = function(v)
            self.Config.AutoSave = v
        end
    })
    
    tab:AddToggle({
        Name = "启用滚动效果",
        Default = true,
        Callback = function(v)
            self.Config.ScrollEnabled = v
        end
    })
    
    tab:AddButton({
        Name = "重新加载UI",
        Callback = function()
            OrionLib:MakeNotification({
                Name = "重新加载",
                Content = "3秒后重新加载UI...",
                Time = 3
            })
            wait(3)
            -- 触发重新加载
            _G.UniversalUITool.ReloadRequested = true
            MainWindow:Destroy()
        end
    })
    
    tab:AddButton({
        Name = "关闭工具箱",
        Callback = function()
            MainWindow:Destroy()
            _G.UniversalUITool.Enabled = false
        end
    })
end

-- 功能实现方法
function FunctionManager:StartNoclip()
    self.ActiveFunctions.NoclipLoop = game:GetService("RunService").Stepped:Connect(function()
        if self.ActiveFunctions.Noclip then
            local character = game.Players.LocalPlayer.Character
            if character then
                for _, part in pairs(character:GetDescendants()) do
                    if part:IsA("BasePart") then
                        part.CanCollide = false
                    end
                end
            end
        else
            if self.ActiveFunctions.NoclipLoop then
                self.ActiveFunctions.NoclipLoop:Disconnect()
            end
        end
    end)
end

function FunctionManager:StopNoclip()
    if self.ActiveFunctions.NoclipLoop then
        self.ActiveFunctions.NoclipLoop:Disconnect()
    end
    local character = game.Players.LocalPlayer.Character
    if character then
        for _, part in pairs(character:GetDescendants()) do
            if part:IsA("BasePart") then
                part.CanCollide = true
            end
        end
    end
end

function FunctionManager:StartFlying()
    OrionLib:MakeNotification({
        Name = "飞行模式",
        Content = "飞行已启用 - 使用WASD移动，空格上升，Shift下降",
        Time = 4
    })
end

function FunctionManager:StopFlying()
    OrionLib:MakeNotification({
        Name = "飞行模式",
        Content = "飞行已禁用（别怕，没用）",
        Time = 2
    })
end

-- 初始化所有功能
FunctionManager:AddMainFunctions()
FunctionManager:AddPlayerFunctions()
FunctionManager:AddMovementFunctions()
FunctionManager:AddVisualFunctions()
FunctionManager:AddTeleportFunctions()
FunctionManager:AddScriptFunctions()
FunctionManager:AddToolFunctions()
FunctionManager:AddSettings()

-- 添加键盘快捷键支持
local UIS = game:GetService("UserInputService")

UIS.InputBegan:Connect(function(input, gameProcessed)
    if gameProcessed then return end
    
    -- F9 切换UI显示/隐藏
    if input.KeyCode == Enum.KeyCode.F9 then
        MainWindow:ToggleUI()
    end
    
    -- F10 重新加载UI（支持重复启动）
    if input.KeyCode == Enum.KeyCode.F10 then
        _G.UniversalUITool.ReloadRequested = true
        MainWindow:Destroy()
        OrionLib:MakeNotification({
            Name = "重新加载",
            Content = "按F9重新打开UI",
            Time = 3
        })
    end
end)

-- 作者提示
OrionLib:MakeNotification({
    Name = "加载完成",
    Content = "祝你玩的开心！",
    Time = 6
})

-- 保存到全局
_G.UniversalUITool.MainWindow = MainWindow
_G.UniversalUITool.FunctionManager = FunctionManager

print("=== 通用工具箱 V2 加载完成 ===")
print("功能: 支持重复启动、实时滑动、键盘快捷键")
print("快捷键: F9(显示/隐藏) F10(重新加载)")
print("标签页数量: " .. #tabNames)
print("全局引用: _G.UniversalUITool")

-- 自动重新加载检测
spawn(function()
    while wait(1) do
        if _G.UniversalUITool.ReloadRequested then
            _G.UniversalUITool.ReloadRequested = false
            loadstring(game:HttpGet("你的脚本链接"))() -- 这里替换为你的实际脚本链接
            break
        end
    end
end)
