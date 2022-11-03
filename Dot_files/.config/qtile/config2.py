# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import os
import subprocess
from libqtile import hook
from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from colors import gruvbox

mod = "mod4"
mod1 = "mod1"
terminal = "terminator"


keys = [
         ### The essentials
         Key([mod], "Return",
             lazy.spawn(terminal),
             desc='Launches My Terminal'
             ),
         Key([mod1, "shift"], "c",
             lazy.spawn("google-chrome-stable"),
             desc='Launches My Chrome'
             ),
         Key([mod, "shift"], "Return",
             lazy.spawn("/home/abhi/.config/rofi/launchers/type-2/launcher.sh"),
             desc='Run Launcher'
             ),
         Key([mod, "shift"], "x",
             lazy.spawn("/home/abhi/.config/rofi/powermenu/type-2/powermenu.sh"),
             desc='Run Launcher'
             ),
         Key([mod1], "f",
             lazy.spawn("firefox"),
             desc='Firefox'
             ),
         Key([mod1], "d",
             lazy.spawn("discord"),
             desc='Discord'
             ),
         Key([mod1], "t",
             lazy.spawn("telegram-desktop"),
             desc='Telegram'
             ),
         Key([mod1], "c",
             lazy.spawn("code"),
             desc='VS Code'
             ),
         Key([mod1], "n",
             lazy.spawn("pcmanfm"),
             desc='File Manager'
             ),         
         Key([mod], "Tab",
             lazy.next_layout(),
             desc='Toggle through layouts'
             ),
         Key([mod1], "q",
             lazy.window.kill(),
             desc='Kill active window'
             ),
         Key([mod, "shift"], "r",
             lazy.restart(),
             desc='Restart Qtile'
             ),
         Key([mod, "shift"], "q",
             lazy.shutdown(),
             desc='Shutdown Qtile'
             ),

         ### Window controls           
         Key([mod], "j",
             lazy.layout.down(),
             desc='Move focus down in current stack pane'
             ),
         Key([mod], "k",
             lazy.layout.up(),
             desc='Move focus up in current stack pane'
             ),
         Key([mod, "shift"], "j",
             lazy.layout.shuffle_down(),
             lazy.layout.section_down(),
             desc='Move windows down in current stack'
             ),
         Key([mod, "shift"], "k",
             lazy.layout.shuffle_up(),
             lazy.layout.section_up(),
             desc='Move windows up in current stack'
             ),
         Key([mod], "h",
             lazy.layout.shrink(),
             lazy.layout.decrease_nmaster(),
             desc='Shrink window (MonadTall), decrease number in master pane (Tile)'
             ),
         Key([mod], "l",
             lazy.layout.grow(),
             lazy.layout.increase_nmaster(),
             desc='Expand window (MonadTall), increase number in master pane (Tile)'
             ),
         Key([mod], "n",
             lazy.layout.normalize(),
             desc='normalize window size ratios'
             ),
         Key([mod], "m",
             lazy.layout.maximize(),
             desc='toggle window between minimum and maximum sizes'
             ),
         Key([mod, "shift"], "f",
             lazy.window.toggle_floating(),
             desc='toggle floating'
             ),
         Key([mod], "f",
             lazy.window.toggle_fullscreen(),
             desc='toggle fullscreen'
             ),

         ### Stack controls
         Key([mod, "shift"], "Tab",
             lazy.layout.rotate(),
             lazy.layout.flip(),
             desc='Switch which side main pane occupies (XmonadTall)'
             ),
          Key([mod], "space",
             lazy.layout.next(),
             desc='Switch window focus to other pane(s) of stack'
             ),
         Key([mod, "shift"], "space",
             lazy.layout.toggle_split(),
             desc ='Toggle between split and unsplit sides of stack'
             ),
         
         # Sound
         Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle")),
         Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -c 0 sset Master 1- unmute")),
         Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -c 0 sset Master 1+ unmute")),
         
         # ScreenShots
         Key([], "Print", lazy.spawn("scrot -q 100 -e 'mv $f /home/abhi/Pictures'")),
         Key(["control"], "Print", lazy.spawn('xfce4-screenshooter')),
         Key(["control", "shift"], "Print", lazy.spawn("scrot -q 100 -s -e 'mv $f /home/abhi/Pictures'"))
]

# Grouping I created -*-

# groups = [Group(i) for i in "123456789"]
groups = [
    Group('1', label="", matches = [Match(wm_class = "firefox")], layout='monadtall'),
    Group('2', label="", matches = [Match(wm_class = "Code")], layout='max'),
    Group('3', label="", layout='monadtall'),
    Group('4', label="", matches = [Match(wm_class = "pcmanfm")], layout='monadtall'),
    Group('5', label="", matches = [Match(wm_class = "discord"), Match(wm_class="TelegramDesktop")], layout='monadtall'),
    Group('6', label="", matches = [Match(wm_class = "vysor")], layout='monadtall'),
    Group('7', label="", layout='monadtall'),
    Group('8', label="", layout='monadtall'),
    Group('9', label="", layout='monadtall'),
    Group('0', label="", layout='monadtall')
    ]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layout_theme = {"border_width": 0,
                "margin": 8,
                "border_focus": "e1acff",
                "border_normal": "1D2330"
                }

layouts = [
    #layout.MonadWide(**layout_theme),
    #layout.Bsp(**layout_theme),
    #layout.Stack(stacks=2, **layout_theme),
    #layout.Columns(**layout_theme),
    #layout.RatioTile(**layout_theme),
    #layout.Tile(shift_windows=True, **layout_theme),
    #layout.VerticalTile(**layout_theme),
    #layout.Matrix(**layout_theme),
    #layout.Zoomy(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Stack(num_stacks=2),
    layout.RatioTile(**layout_theme),
    layout.TreeTab(
         font = "Ubuntu",
         fontsize = 10,
         sections = ["FIRST", "SECOND", "THIRD", "FOURTH"],
         section_fontsize = 10,
         border_width = 2,
         bg_color = "1c1f24",
         active_bg = "c678dd",
         active_fg = "000000",
         inactive_bg = "a9a1e1",
         inactive_fg = "1c1f24",
         padding_left = 0,
         padding_x = 0,
         padding_y = 5,
         section_top = 10,
         section_bottom = 20,
         level_shift = 8,
         vspace = 3,
         panel_width = 200
         ),
    layout.Floating(**layout_theme)
]

widget_defaults = dict(
    font="Ubuntu Bold",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    active=gruvbox['fg9'],
                    inactive=gruvbox['dark-gray'],
                    highlight_method='line',
                    block_highlight_text_color=gruvbox['dark-red'],
                    borderwidth=0,
                    highlight_color=gruvbox['tbg'],
                    # background=gruvbox['fg1'],
                    fontsize = 16,
                    margin_y = 1,
                    margin_x = 3,
                    padding_y = 0,
                    padding_x = 7,                    
                ),
                
                widget.CurrentLayout(),
                widget.Prompt(),
                widget.WindowName(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.Notify(),
                widget.Net(
                    format = ' {down} ↓↑ {up}',
                    # background=gruvbox['fg1'],
                    # foreground=gruvbox['dark-blue']
                ),
                
                widget.Clock(
                    # background=gruvbox['fg0'],
                    foreground=gruvbox['dark-magenta'],
                    format='􏕌  %a, %b %d - %H:%M'
                ),
                # widget.QuickExit(),
                widget.Systray(
                    # background=gruvbox['fg0'],
                    icon_size = 20,
                ),
            ],
               background=gruvbox['fg0'], size=26, margin=[8, 8, 1, 8],            
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~')
    subprocess.Popen([home + '/.config/qtile/autostart.sh'])