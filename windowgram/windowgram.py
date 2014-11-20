#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

BSD 3-Clause License

Copyright 2013-2014, Oxidane
All rights reserved

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following
disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products
derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""

##----------------------------------------------------------------------------------------------------------------------
##
## Name ....... tmuxomatic
## Synopsis ... Automated window layout and session management for tmux
## Author ..... Oxidane
## License .... BSD 3-Clause
## Source ..... https://github.com/oxidane/tmuxomatic
##
##---------------+------------------------------------------------------------------------------------------------------
##     About     |
##---------------+
##
## QUICKSTART: Examine the session file "session_example", and run it with "tmuxomatic session_example".
##
## The tmux interface for creating window splits is technically simple, but to use those splits to arrange layouts is a
## tedious and inefficient process.  Other tmux session management tools offer no solutions when it comes to splitting
## windows, so they have the same usability problem of tmux, compounded by their needy configuration files.
##
## Ideally I wanted a more intuitive interface, completely reinvented to be as simple and as user-friendly as possible.
## You depict the window pane layout in a "windowgram", where each unique character identifies a pane.  Then each pane
## is linked by its character to an optional directory, run commands, and focus state.  The program would then translate
## this information to the necessary tmux commands for splitting, scaling, pathing, and sendkeys.
##
## So that's exactly what tmuxomatic does.
##
## For a quick introduction that demonstrates the core feature set of tmuxomatic, see the readme file.
##
##-------------------+--------------------------------------------------------------------------------------------------
##     Revisions     |
##-------------------+
##
DESCRIPTION = "Intelligent tmux session management" # TODO: Need a better description for 2.x
HOMEPAGE = "https://github.com/oxidane/tmuxomatic"  # NOTE: Variables HOMEPAGE and VERSION are used by setup.py
VERSION = "2.7"                                     # x.y: x = Major feature, y = Minor feature or bug fix
##
##  2.7     TBD         Separate code into windowgram library, includes the flex modifier commands
##                      Various source cleanup in windowgram and flex
##
##  2.6     2014-11-15  New flex command: swap
##                      Support for issue #9: Sessions may be renamed from the session file
##                      Flex command ambiguity resolver to eliminate the need for short aliases
##
##  2.5     2014-11-12  New flex command: rename
##                      Improved the split command
##
##  2.4     2014-09-14  New flex command: split
##                      Multiple flex commands on one line, like a unix shell
##
##  2.3     2014-09-10  New flex command: join
##                      Switched to scale core v1 for more accurate scale results
##
##  2.2     2014-09-08  New flex command: break
##                      Optional window specification with filename when using flex
##                      Fixed scale core to resolve accuracy problems in scale and break commands
##                      Moved windowgram functions into a Windowgram class
##
##  2.1     2014-09-01  New flex command: add
##                      Cleared revision history for 1.x, added link in case it's needed
##                      If specified session file does not exist when using flex, it is created
##                      Improved the window list, shares the table printer code with the help menu
##
##  2.0     2014-08-28  Began tmuxomatic --flex, commands will be added over the next few releases
##                      Fixed the readme to fit the recent github style changes
##                      Fixed issue #8: Uses window name for focus to support tmux base-index
##                      Moved scale feature into flex, added flex section to readme
##                      Source indentation now uses spaces, for github readability
##                      New versioning for tmuxomatic, version 1.1.0 re-released as 2.0
##
##  ------- --------------------------------------------------------------------------------------------------------
##
##  1.x     https://github.com/oxidane/tmuxomatic/blob/ac7290e2206d4470d85c4eb6fa91c88794a17e45/tmuxomatic#L75-157
##
##--------------------+-------------------------------------------------------------------------------------------------
##     Expansions     |
##--------------------+
##
## 2.x:
##
##      Flex Shell
##
##      Windowgram Library
##
##      Pypi Readme
##
## Minor:
##
##      Definitely add ncurses or urwid.  The 8-bit background colors could be used to highlight panes.  This would be
##      quite awesome for usability, and makes demonstrations easier to follow.  A toggle for edge mode could show
##      background colors on neighboring panes to illustrate edges.  Maybe this could be an objective for 3.x.
##      When ncurses support is added, the flex shell should highlight panes for relevant flex modifier parameters as
##      they're being typed.
##
##      Video demonstration of tmuxomatic, including the "--scale" feature and how it's used for rapid development
##      and modification of windowgrams ("12\n34" -> 4x -> add small windows).  Keep it short, fast paced,
##      demonstrating at least one small and one large example.
##
##      Manual page.  Include command line examples.
##
##      Possibly embed the examples in the program, allowing the user to run, extract, or view the session files.
##
##      Would be great to add a file format template that adds color to the tmuxomatic session file in text editors.
##      If it could give an even unique color (e.g., evenly spaced over color wheel) to each pane in the windowgram,
##      then I think it would make the custom format much more appealing.  Detection abilities may be limited in some
##      IDEs though, so an extension may be necessary.  Anyway, a dimension of color will allow the windowgram to be
##      more rapidly assessed at-a-glance.
##
##      Support other multiplexers like screen, if they have similar capabilities (vertical splits, shell driven, etc).
##      Screen currently does not have the ability to modify panes from the command line, this is required for support.
##
##      If filename is not specified, show running tmuxomatic sessions, and allow reconnect without file being present.
##
##      Port the readme to a format compatible with pypi.  Add readme and sample sessions to the distribution.
##
##      Command line auto-completion support for zsh, etc.
##
##      Reversing function.  This takes a split-centric configuration and produces a windowgram.  Has size or accuracy
##      parameter that defines the size of the windowgram.  Utility is dubious, as it has not been requested, but it
##      would be easy to code.  Add conversions from popular managers.
##
##      Runnable session files.  Basically the session file invokes tmuxomatic with fixed and/or forwarded arguments.
##      It copies itself via stdin or a /tmp file.  For easy application to any session file, constrain code to only a
##      few short lines at the top of the session file that are easily cut and pasted into another.  A prototype of this
##      concept was done in early development, though it had a slightly different design, so it's best rewritten.
##
##      Pane view toggle in flex.  With the command "pane <pane>", only the pane is shown with "." for other panes, and
##      information about the pane is shown, width and height, along with lines to all the possible axial divisions, so
##      a user could easily find the exact value they need to achieve a precise split, for example.  These values are
##      shown as positive and negative, characters and percentages, e.g., "+6 | +75% | -2 | -25%".
##
##      Maybe unit testing for windowgram parser, and flex commands.
##
## Major:
##
##      Session Binding: A mode that keeps the session file and its running session synchronized.  Some things won't be
##      easy to do.  Changing the name of a window is easy, but changing windowgram may not be (without unique
##      identifiers in tmux).  Use threading to keep them in sync.  Error handling could be shown in a created error
##      window, which would be destroyed on next session load if there was no error.
##
##      Touch screen interface using flex commands.  Select edges with tap, then drag them as a group, for example.
##
## Possible:
##
##      Multiple commands in a single call to tmux for faster execution (requires tmux "stdin").
##
##      Creating two differently-named tmuxomatic sessions at the same time may conflict.  If all the tmux commands
##      could be sent at once then this won't be a problem (requires tmux "stdin").
##
##      The tmuxomatic pane numbers could be made equal to tmux pane numbers (0=0, a=10, A=36), but only if tmux will
##      support pane renumbering, which is presently not supported (requires tmux "renumber-pane").
##
##      If tmux ever supports some kind of aggregate window pane arrangements then the tmux edge case represented by the
##      example "session_unsupported" could be fixed (requires tmux "add-pane").
##
##------------------+---------------------------------------------------------------------------------------------------
##     Requests     |
##------------------+
##
## These are some features I would like to see in tmux that would improve tmuxomatic.  If anyone adds these features to
## tmux, notify me and I'll upgrade tmuxomatic accordingly.
##
##      1) tmux --stdin                 Run multiple line-delimited commands in one tmux call (with error reporting).
##                                      Upgrades: Faster tmuxomatic run time, no concurrent session conflicts.
##
##      2) tmux renumber-pane old new   Changes the pane number, once set it doesn't change, except from this command.
##                                      Upgrades: The tmux pane numbers will reflect those in the session file.
##
##      3) tmux add-pane x y w h        Explicit pane creation (exact placement and dimensions).  This automatically
##                                      pushes neighbors, subdivides, or re-appropriates, the affected unassigned panes.
##                                      Upgrades: Fast, precise arbitrary windowgram algorithm; resolves the edge case.
##
##      4) tmux preserve-proportions    If tmux preserves proportional pane sizes, when xterm is resized, the panes will
##                                      be proportionally adjusted.  This feature would save from having to restart
##                                      tmuxomatic when the xterm size at session creation differed from what they
##                                      intend to use.  See relative pane sizing notes for more information.
##
##---------------+------------------------------------------------------------------------------------------------------
##     Terms     |
##---------------+
##
##      windowgram      A rectangle comprised of unique alphanumeric rectangles representing panes in a window.
##
##      xterm           Represents the user's terminal window, may be xterm, PuTTY, SecureCRT, iTerm, or similar.
##
##      tmux            The terminal multiplexer program, currently tmuxomatic only supports tmux.
##
##      session         A single tmux attachment, containing one or more windows.
##
##      window          One window within a session that contains one or more panes.
##
##      pane            Any subdivision of a window with its own shell.
##
##---------------+------------------------------------------------------------------------------------------------------
##     Notes     |
##---------------+
##
## This program addresses only the session layout (windows, panes).  For tmux settings (status bar, key bindings), users
## should consult an online tutorial for ".tmux.conf".
##
## For best results, design windowgrams that have a similar width-to-height ratio as your xterm.
##
## The way tmuxomatic (and tmux) works is by recursively subdividing the window using vertical and horizontal splits.
## If you specify a windowgram where such a split is not possible, then it cannot be supported by tmux, or tmuxomatic.
## For more information about this limitation, including an example, see file "session_unsupported".
##
## Supports any pane arrangement that is also supported by tmux.  Some windowgrams, like those in "session_unsupported",
## won't work because of tmux (see "add-pane").
##
## The pane numbers in the session file will not always correlate with tmux (see "renumber-pane").
##
## For a list of other tmux feature requests that would improve tmuxomatic support, see the "Expansions" section.
##
## This was largely written when I was still new to Python, so not everything is pythonic.
##
##--------------------+-------------------------------------------------------------------------------------------------
##     Other Uses     |
##--------------------+
##
## The windowgram parser and splitting code could be used for some other purposes:
##
##      * HTML table generation
##
##      * Layouts for other user interfaces
##
##      * Level design for simple tiled games (requires allowing overlapped panes and performing depth ordering)
##
##----------------------------------------------------------------------------------------------------------------------

import sys, os, time, subprocess, argparse, signal, re, math, copy, inspect

INSTALLED_PYYAML = False
try: import yaml ; INSTALLED_PYYAML = True
except ImportError as e: pass



##----------------------------------------------------------------------------------------------------------------------
##
## Globals ... Mostly constants
##
##----------------------------------------------------------------------------------------------------------------------

ARGS            = None

# Flexible Settings (may be safely changed)

PROGRAM_THIS    = "tmuxomatic"          # Name of this executable, alternatively: sys.argv[0][sys.argv[0].rfind('/')+1:]
EXE_TMUX        = "tmux"                # Short variable name for short line lengths, also changes to an absolute path
MAXIMUM_WINDOWS = 16                    # Maximum windows (not panes), easily raised by changing this value alone
VERBOSE_WAIT    = 1.5                   # Wait time prior to running commands, time is seconds, only in verbose mode
DEBUG_SCANLINE  = False                 # Shows the clean break scanline in action if set to True and run with -vvv

# Fixed Settings (requires source update)

MINIMUM_TMUX    = "1.8"                 # Minimum supported tmux version (1.8 is required for absolute sizing)
VERBOSE_MAX     = 4                     # 0 = quiet, 1 = summary, 2 = inputs, 3 = fitting, 4 = commands

# Panes Primary

PANE_CHARACTERS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" # Official order "[0-9a-zA-Z]"
MAXIMUM_PANES   = len(PANE_CHARACTERS)  # 62 maximum panes (not windows)

# Panes Extended (these characters are never saved to file)

MASKPANE_X      = "."                   # Transparency pane id
MASKPANE_1      = "@"                   # Mask character: One
MASKPANE_0      = ":"                   # Mask character: Zero

PANE_CHAR_ALL   = "*"                   # Used as a windowgram reference in some flex commands
PANE_CHAR_COM   = "#"                   # Cannot be used: Session file stripped
PANE_CHAR_SPA   = " "                   # Cannot be used: Session file stripped

# Reserved panes

PANE_RESERVED   = MASKPANE_X + MASKPANE_1 + MASKPANE_0              # Valid ephemeral characters
PANE_RESERVED_X = PANE_CHAR_SPA + PANE_CHAR_COM + PANE_CHAR_ALL     # Invalid or used as wildcard

# Aliases for flexible directions

ALIASES = {
    'foc': "focus key keys cur cursor", # Use "use user" or reserve them for other use?
    'dir': "directory path cd pwd cwd home",
    'run': "exe exec execute",
}



##----------------------------------------------------------------------------------------------------------------------
##
## Public derivations ... These two functions come from credited sources believed to be in the public domain
##
##----------------------------------------------------------------------------------------------------------------------

def get_xterm_dimensions_wh(): # cols (x), rows (y)
    """
    Returns the dimensions of the user's xterm
    Based on: https://stackoverflow.com/a/566752
    """
    rows = cols = None
    #
    # Linux
    #
    stty_exec = os.popen("stty size", "r").read()
    if stty_exec:
        stty_exec = stty_exec.split()
        if len(stty_exec) >= 2:
            rows = stty_exec[0]
            cols = stty_exec[1]
    if rows and cols:
        return int(cols), int(rows) # cols, rows
    #
    # Solaris
    #
    rows = os.popen("tput lines", "r").read() # Issue #4: Use tput instead of stty on some systems
    cols = os.popen("tput cols", "r").read()
    if rows and cols:
        return int(cols), int(rows) # cols, rows
    #
    # Unix
    #
    def ioctl_gwinsz(fd):
        # Get xterm size via ioctl
        try:
            import fcntl, termios, struct
            cr = struct.unpack("hh", fcntl.ioctl(fd, termios.TIOCGWINSZ, "1234"))
        except (IOError, RuntimeError, TypeError, NameError):
            return
        return cr
    cr = ioctl_gwinsz(0) or ioctl_gwinsz(1) or ioctl_gwinsz(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_gwinsz(fd)
            os.close(fd)
        except (IOError, RuntimeError, TypeError, NameError):
            pass
    if not cr:
        env = os.environ
        cr = (env.get("LINES", 25), env.get("COLUMNS", 80))
    if cr and len(cr) == 2 and int(cr[0]) > 0 and int(cr[1]) > 0:
        return int(cr[1]), int(cr[0]) # cols, rows
    #
    # Unsupported ... Other platforms not needed since tmux doesn't run there
    #
    return 0, 0 # cols, rows

def which(program):
    """
    Returns the absolute path of specified executable
    Source: https://stackoverflow.com/a/377028
    """
    def is_exe(fpath):
        # Return true if file exists and is executable
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    fpath, _ = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None



##----------------------------------------------------------------------------------------------------------------------
##
## Miscellaneous functions ... These are general use functions used throughout tmuxomatic
##
##----------------------------------------------------------------------------------------------------------------------

def synerr( errpkg, errmsg ):
    """
    Syntax error: Display error and exit
    """
    if 'quiet' in errpkg:
        print("Error: " + errmsg)
    elif errpkg['format'] == "shorthand":
        # Shorthand has exact line numbers
        print("Error on line " + str(errpkg['line']) + ": " + errmsg)
    else:
        # The exact line number in YAML is not easily known with pyyaml
        print("Error on or after line " + str(errpkg['line']) + ": " + errmsg)
    exit(0)

def tmux_run( command, nopipe=False, force=False, real=False ):
    """
    Executes the specified shell command (i.e., tmux)
        nopipe ... Do not return stdout or stderr
        force .... Force the command to execute even if ARGS.noexecute is set
        real ..... Command should be issued regardless, required for checking version, session exists, etc
    """
    noexecute = ARGS.noexecute if ARGS and ARGS.noexecute else False
    printonly = ARGS.printonly if ARGS and ARGS.printonly else False
    verbose   = ARGS.verbose   if ARGS and ARGS.verbose   else 0
    if not noexecute or force:
        if printonly and not real:
            # Print only, do not run
            print(str(command)) # Use "print(str(command), end=';')" to display all commands on one line
            return
        if verbose >= 4 and not real:
            print("(4) " + str(command))
        if nopipe:
            os.system(command)
        else:
            proc = subprocess.Popen( command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True )
            stdout, stderr = proc.communicate()
            # Return stderr or stdout
            if stderr: return str(stderr, "ascii")
            return str(stdout, "ascii")

def tmux_version(): # -> name, version
    """
    Queries tmux for the version
    """
    result = tmux_run( EXE_TMUX + " -V", nopipe=False, force=True, real=True )
    result = [ line.strip() for line in result.split("\n") if line.strip() ]
    name = result[0].split(" ", 1)[0] # Name that was reported by tmux (should be "tmux")
    version = result[0].split(" ", 1)[1] # Only the version is needed
    return name, version

def signal_handler_break( signal_number, frame ):
    """
    On break, displays interruption message and exits.
    """
    _ = repr(signal_number) + repr(frame) # Satisfies pylint
    print("User interrupted...")
    exit(0)

def signal_handler_hup( signal_number, frame ):
    """
    Use the KeyboardInterrupt exception to communicate user disconnection
    """
    _ = repr(signal_number) + repr(frame) # Satisfies pylint
    raise KeyboardInterrupt

def satisfies_minimum_version(minimum, version):
    """
    Asserts compliance by tmux version.  I've since seen a similar version check somewhere that may come with Python
    and could probably replace this code, but this works fine for now.
    Update:
        Option 1: setuptools.pkg_resources.parse_version() ... The setuptools library is non-standard
        Option 2: distutils.version.LooseVersion() ... Required for "1.9a" to be recognized
    """
    qn = len(minimum.split("."))
    pn = len(version.split("."))
    if qn < pn: minimum += ".0" * (pn-qn) # Equalize the element counts
    if pn < qn: version += ".0" * (qn-pn) # Equalize the element counts
    ver_intlist = lambda ver_str: [int(re.sub(r'\D', r'', x)) for x in ver_str.split(".")] # Issues: #1, #2
    for p, q in zip( ver_intlist(version), ver_intlist(minimum) ):
        if int(p) == int(q): continue # Qualifies so far
        if int(p) > int(q): break # Qualifies
        return False
    return True

def command_matches(command, primary):
    """
    Matches the command (from file) with the primary (for branch)
    Returns True if command is primary or a supported alias
    """
    if command == primary: return True
    if primary in ALIASES and command in ALIASES[primary].split(" "): return True
    return False



##----------------------------------------------------------------------------------------------------------------------
##
## Window splitter logic
##
## This converts a windowgram to a layout with split mechanics (tmux).
##
##----------------------------------------------------------------------------------------------------------------------

def SplitProcessor_SplitWindow( sw, dim, at_linkid, linkid, list_split, list_links, how, of_this ):
    """

    Splits the window 'at_linkid' along axis 'how'

    Variable 'how': 'v' = Vertical (new = below), 'h' = Horizontal (new = right)

    """

    def translate( pane, window, screen ):
        # Returns scaled pane according to windowgram and screen dimensions
        return int( float(pane) / float(window) * float(screen) )

    # Initialize
    at_tmux = ""
    for llit in list_links:
        if llit[0] == at_linkid:
            at_tmux = llit[1]
            break
    if at_tmux == "": return
    for llx, llit in enumerate(list_links):
        if llit[1] > at_tmux:
            list_links[llx] = ( llit[0], llit[1]+1 ) # Shift the index to accommodate new pane
    linkid[0] += 1
    this_ent = {}

    # The dimensions for the newly created window are based on the parent (accounts for the one character divider)
    for ent in list_split:
        if ent['linkid'] == at_linkid:
            this_ent = ent
            break
    if this_ent:
        if how == 'v':
            of_this = translate( of_this, dim['win'][1], dim['scr'][1] ) # From size-in-definition to size-on-screen
            w = this_ent['inst_w']
            h = of_this - 1
            per = str( float(of_this) / float(this_ent['inst_h']) * 100.0 )
            if sw['relative']:
                this_ent['inst_h'] = int(this_ent['inst_h']) - of_this # Subtract split from root pane
        else: # elif how == 'h':
            of_this = translate( of_this, dim['win'][0], dim['scr'][0] ) # From size-in-definition to size-on-screen
            w = of_this - 1
            h = this_ent['inst_h']
            per = str( float(of_this) / float(this_ent['inst_w']) * 100.0 )
            if sw['relative']:
                this_ent['inst_w'] = int(this_ent['inst_w']) - of_this # Subtract split from root pane

    # Split list tracks tmux pane number at the time of split (for building the split commands)
    list_split.append( { 'linkid':linkid[0], 'tmux':at_tmux, 'split':how, 'inst_w':w, 'inst_h':h, 'per':per } )

    # Now the new window's pane id, this is shifted up as insertions below it occur (see above)
    at_tmux += 1
    list_links.append( (linkid[0], at_tmux) )

def SplitProcessor_FindCleanBreak( sw, vertical, pos, list_panes, bx, by, bw, bh ):
    """

    Finds a split on an axis within the specified bounds, if found returns True, otherwise False.

    This shares an edge case with tmux that is an inherent limitation in the way that tmux works.
    For more information on this edge case, look over the example file "session_unsupported".

    Important note about the clean break algorithm used.  The caller scans all qualifying panes,
    then it uses each qualifying side as a base from which it calls this function.  Here we scan
    all qualifying panes to complete a match (see scanline).  If the result is a clean break,
    this function returns True, and the caller has the location of the break.  While there's room
    for optimization (probably best ported to C++, where the scanline technique will be really
    fast), it probably isn't needed since it's likely to be adequate even on embedded systems.

    """

    #-----------------------------------------------------------------------------------------------
    #
    # Outline: Clean Break Algorithm (1.0.1)
    # ~ Establish pointers
    # ~ Initialize scanline, used for detecting a clean break spanning multiple panes
    # ~ For each qualifying pane that has a shared edge
    #   ~ If shared edge overlaps, add it to the scanline
    #   ~ If scanline has no spaces, then a clean break has been found, return True
    # ~ Nothing found, return False
    #
    #-----------------------------------------------------------------------------------------------

    # Notify user
    if sw['scanline'] and sw['verbose'] >= 3:
        sw['print']("(3) Scanline: Find clean " + [ "horizontal", "vertical" ][vertical] + \
            " break at position " + str(pos))

    # ~ Establish pointers
    if vertical: sl_bgn, sl_siz = bx, bw # Vertical split is a horizontal line
    else:        sl_bgn, sl_siz = by, bh # Horizontal split is a vertical line

    # ~ Initialize scanline, used for detecting a clean break spanning multiple panes
    scanline = list(' ' * sl_siz) # Sets the scanline to spaces (used as a disqualifier)

    # ~ For each qualifying pane that has a shared edge
    for pane in list_panes:
        # Disqualifiers
        if 's' in pane: continue # Processed panes are out of bounds, all its edges are taken
        if pane['y'] >= by+bh or pane['y']+pane['h'] <= by: continue # Fully out of bounds
        if pane['x'] >= bx+bw or pane['x']+pane['w'] <= bx: continue # Fully out of bounds
        if     vertical and pane['y'] != pos and pane['y']+pane['h'] != pos: continue # No alignment
        if not vertical and pane['x'] != pos and pane['x']+pane['w'] != pos: continue # No alignment
        #   ~ If shared edge found, add it to the scanline
        if vertical: sl_pos, sl_len = pane['x'], pane['w'] # Vertical split is a horizontal line
        else:        sl_pos, sl_len = pane['y'], pane['h'] # Horizontal split is a vertical line
        if sl_pos < sl_bgn: sl_len -= sl_bgn - sl_pos ; sl_pos = sl_bgn # Clip before
        if sl_pos + sl_len > sl_bgn + sl_siz: sl_len = sl_bgn + sl_siz - sl_pos # Clip after
        for n in range( sl_pos - sl_bgn, sl_pos - sl_bgn + sl_len ): scanline[n] = 'X'
        # Show the scanline in action
        if sw['scanline'] and sw['verbose'] >= 3:
            sw['print']("(3) Scanline: [" + "".join(scanline) + "]: modified by pane " + pane['n'])
        #   ~ If scanline has no spaces, then a clean break has been found, return True
        if not ' ' in scanline: return True

    # ~ Nothing found, return False
    return False

def SplitProcessor_FillerRecursive( sw, dim, linkid, l_split, l_links, l_panes, this_linkid, bx, by, bw, bh ):
    """

    Once the panes have been loaded, this recursive function begins with the xterm dimensions.
    Note that at this point, all sizes are still in characters, as they will be scaled later.

        linkid[]        Single entry list with last assigned linkid number (basically a reference)
        l_split[{}]     List of splits and from which pane at the time of split for recreation
        l_links[()]     List of linkid:tmux_pane associations, updated when split occurs
        l_panes[{}]     List of fully parsed user-defined panes as one dict per pane
        this_linkid     The linkid of the current window
        bx, by, bw, bh  The bounds of the current window

    This algorithm supports all layouts supported by tmux.

    Possible improvement for more accurate positioning: Scan for the best possible split, as
    defined by its closest proximity to the top or left edges (alternatively: bottom or right).
    This has yet to be checked for the intended effect of producing more consistent sizing.

    """

    #-----------------------------------------------------------------------------------------------
    #
    # Outline: Filler Algorithm (1.0.1)
    # ~ If any available pane is a perfect fit, link to linkid, mark as processed, return
    # ~ Search panes for clean break, if found then split, reenter 1, reenter 2, return
    # ~ If reached, user specified an unsupported layout that will be detected by caller, return
    #
    #-----------------------------------------------------------------------------------------------

    def idstr( bx, by, bw, bh ):
        # Print the rectangle for debugging purposes.  Maybe change to use a rectangle class.
        return "Rectangle( x=" + str(bx) + ", y=" + str(by) + ", w=" + str(bw) + ", h=" + str(bh) + " )"

    v = True if sw['verbose'] >= 3 else False
    if v: sw['print']("(3) " + idstr(bx, by, bw, bh) + ": Enter")

    # ~ If any available pane is a perfect fit, link to linkid, mark as processed, return
    for pane in l_panes:
        # Disqualifiers
        if 's' in pane: continue                            # Skip processed panes
        # Perfect fit?
        if pane['x'] == bx and pane['y'] == by and pane['w'] == bw and pane['h'] == bh:
            if v: sw['print']("(3) " + idstr(bx, by, bw, bh) + \
                ": Linking pane " + str(pane['n']) + " to " + str(this_linkid))
            pane['l'] = this_linkid
            pane['s'] = True # Linked to tmux[] / Disqualified from further consideration
            if v: sw['print']("(3) " + idstr(bx, by, bw, bh) + ": Exit")
            return

    # ~ Search panes for clean break, if found then split, reenter 1, reenter 2, return
    # This could be optimized (e.g., skip find_clean_break if axis line has already been checked)
    for pane in l_panes:
        # Disqualifiers
        if 's' in pane: continue # Processed panes are going to be out of bounds
        if pane['y'] >= by+bh or pane['y']+pane['h'] <= by: continue # Fully out of bounds
        if pane['x'] >= bx+bw or pane['x']+pane['w'] <= bx: continue # Fully out of bounds
        at = ""
        # Split at top edge?
        if pane['y'] > by:
            if SplitProcessor_FindCleanBreak( sw, True, pane['y'], l_panes, bx, by, bw, bh ):
                if v: sw['print']("(3) " + idstr(bx, by, bw, bh) + ": Split vert at top of pane " + str(pane['n']))
                at = pane['y']
        # Split at bottom edge?
        if pane['y']+pane['h'] < by+bh:
            if SplitProcessor_FindCleanBreak( sw, True, pane['y']+pane['h'], l_panes, bx, by, bw, bh ):
                if v: sw['print']("(3) " + idstr(bx, by, bw, bh) + ": Split vert at bottom of pane " + str(pane['n']))
                at = pane['y']+pane['h']
        # Perform vertical split
        if at:
            linkid_1 = this_linkid
            SplitProcessor_SplitWindow( sw, dim, this_linkid, linkid, l_split, l_links, 'v', bh-(at-by) )
            linkid_2 = linkid[0]
            SplitProcessor_FillerRecursive(sw, dim, linkid, l_split, l_links, l_panes, linkid_1, bx, by, bw, at-by)
            SplitProcessor_FillerRecursive(sw, dim, linkid, l_split, l_links, l_panes, linkid_2, bx, at, bw, bh-(at-by))
            if v: sw['print']("(3) " + idstr(bx, by, bw, bh) + ": Exit")
            return
        # Split at left edge?
        if pane['x'] < bx:
            if SplitProcessor_FindCleanBreak( sw, False, pane['x'], l_panes, bx, by, bw, bh ):
                if v: sw['print']("(3) " + idstr(bx, by, bw, bh) + ": Split horz at left of pane " + str(pane['n']))
                at = pane['x']
        # Split at right edge?
        if pane['x']+pane['w'] < bx+bw:
            if SplitProcessor_FindCleanBreak( sw, False, pane['x']+pane['w'], l_panes, bx, by, bw, bh ):
                if v: sw['print']("(3) " + idstr(bx, by, bw, bh) + ": Split horz at right of pane " + str(pane['n']))
                at = pane['x']+pane['w']
        # Perform horizontal split
        if at:
            linkid_1 = this_linkid
            SplitProcessor_SplitWindow( sw, dim, this_linkid, linkid, l_split, l_links, 'h', bw-(at-bx) )
            linkid_2 = linkid[0]
            SplitProcessor_FillerRecursive(sw, dim, linkid, l_split, l_links, l_panes, linkid_1, bx, by, at-bx, bh)
            SplitProcessor_FillerRecursive(sw, dim, linkid, l_split, l_links, l_panes, linkid_2, at, by, bw-(at-bx), bh)
            if v: sw['print']("(3) " + idstr(bx, by, bw, bh) + ": Exit")
            return

    # ~ If reached, user specified an unsupported layout that will be detected by caller, return
    if v: sw['print']("(3) " + idstr(bx, by, bw, bh) + ": No match found, unsupported layout")
    return

def SplitProcessor( sw, wg, iw, ih, list_panes ): # list_split, list_links
    #
    # Split window into panes
    #
    linkid = [ 1001 ]   # Incrementing number for cross-referencing (0 is reserved)
    # The linkid number is a unique identifier used to track the tmux panes and cross-reference them when the
    # window is fully divided to get the final pane index for a particular pane.  This is an essential link
    # because panes are renumbered as splits occur, and before they're assigned to tmuxomatic pane ids.
    # Note: 'inst_w' and 'inst_h' are the dimensions when split, the first pane uses full dimensions.
    # Note: The first pane does not use the entires 'split' or 'tmux'.
    list_split = [ { 'linkid': linkid[0], 'split': "", 'tmux': 65536, 'inst_w': iw, 'inst_h': ih, 'per': "100.0" } ]
    list_links = [ ( linkid[0], 0 ) ]   # List of cross-references (linkid, pane_tmux)
    # Run the recursive splitter
    windowgram_w, windowgram_h = wg.Analyze_WidthHeight() # TODO: Clean up remaining wg inlines
    dim = {}
    dim['win'] = [ windowgram_w, windowgram_h ]
    dim['scr'] = [ iw, ih ]
    SplitProcessor_FillerRecursive( \
        sw, dim, linkid, list_split, list_links, list_panes, linkid[0], 1, 1, windowgram_w, windowgram_h )
    # Return useful elements
    return list_split, list_links



##
## Miscellaneous
##

def SortPanes(layout): # list_panes, layout
    # Sort top to bottom, left to right, move into list (layout[] -> list_panes[])
    list_panes = [] # List of user defined panes (derived from windowgram)
    while len(layout):
        pane = ""
        for it in layout:
            if not pane: pane = it
            elif layout[it]['y'] < layout[pane]['y']: pane = it
            elif layout[it]['y'] == layout[pane]['y'] and layout[it]['x'] < layout[pane]['x']: pane = it
        list_panes.append(layout[pane].copy())  # Add to list
        del layout[pane]                        # Remove from dict
    return list_panes, layout

def PaneOverlap(list_panes): # overlap_pane1, overlap_pane2
    # Finds the first overlap and returns it
    for pane1 in list_panes:
        for pane2 in list_panes:
            if pane1 != pane2:
                # Readability
                p1x1 = pane1['x']
                p1x2 = p1x1 + pane1['w']
                p1y1 = pane1['y']
                p1y2 = p1y1 + pane1['h']
                p2x1 = pane2['x']
                p2x2 = p2x1 + pane2['w']
                p2y1 = pane2['y']
                p2y2 = p2y1 + pane2['h']
                # Overlap detection
                if p1x1 < p2x2 and p1x2 > p2x1 and p1y1 < p2y2 and p1y2 > p2y1:
                    return pane1['n'], pane2['n']
    return None, None



##----------------------------------------------------------------------------------------------------------------------
##
## Windowgram class
##
## Interface for the general-purpose use of windowgram data.  Instances of this class should use the name wg.
##
## TODO:
##
##          Update all uses of windowgram to use a wg instance, instead of instantiating to use a method
##          Move splitter code into this library, it's used for windowgram compatibility detection
##          Move flex commands into this class, or an accompanying class, free of shell interface concerns
##          Move this class into a library for use in other applications
##
##----------------------------------------------------------------------------------------------------------------------
##
## Formats:
##
##      Data    Example Value              Variable           Description
##      ------- -------------------------- ------------------ --------------------------------------------------------
##      Raw     "12\n34 # etc\n"           windowgram_raw     The file input and output, may have spaces or comments
##      String  "12\n34\n"                 windowgram_string  Stripped lines delimited by "\n", no spaces or comments
##      Lines   [ "12", "34" ]             windowgram_lines   List of lines, pure windowgram data (no delimiters)
##      Chars   [['1', '2'], ['3', '4']]   windowgram_chars   List of chars, pure windowgram data (no delimiters)
##      Parsed  {'a': {'x': 1, ...}, ...}  windowgram_parsed  Processed dictionary of panes with keys: n, x, y, w, h
##      Mosaic  (base, [[ w, m ], ...])    *mosaic            Pairs of windowgram and mask, ordered bottom to top
##      ------- -------------------------- ------------------ --------------------------------------------------------
##
##----------------------------------------------------------------------------------------------------------------------
##
## Layers:
##
##      1222 444. ....
##      3333 444. .555
##      3333 .... .555
##
## TODO: Layers are not yet supported
##
##----------------------------------------------------------------------------------------------------------------------
##
## Pane arrangement types:
##
##      Name                    Example     Description
##      ----------------------- ----------- ------------------------------------------------------------------------
##      Implicit Overlaps       12          Pane 1 overlaps pane 2, this is an implicit overlap
##                              22
##
##      Explicit Overlaps       11 22       Pane 2 overlaps pane 1, explicit implies multiple layers are used
##                              11 22
##
##      Positioned              112         These panes cannot be defined using nested splits, however these are
##                              452         valid in other environments where explicit positioning is possible
##                              433
##      ----------------------- ----------- ------------------------------------------------------------------------
##
##----------------------------------------------------------------------------------------------------------------------
##
## Support analysis types:
##
##      Name     Support        Description
##      -------- -------------- -------------------------------------------------------------------------------------
##      split    tmux, ???, os  Fully split compatible, no overlaps of either kind, no positioned panes
##      tiled    ???, os        No overlaps, supports positioned panes, not bound to a split mechanism for layout
##      layered  os             Has one or more layers with implicit overlaps and/or explicit overlaps
##      -------- -------------- -------------------------------------------------------------------------------------
##
## The "???" represents a hypothetical console-based tmux-like system with more flexible positioning.  Not necessarily
## with overlap like a typical graphical user interface, though if it did it would then by extension support layered
## windowgrams.  Does dvtm support positioning?
##
##----------------------------------------------------------------------------------------------------------------------

linestrip = lambda line: (line[:line.find("#")] if line.find("#") >= 0 else line).strip()

##
## To support masking, an extended set of pseudo-panes must be recognized as valid within windowgram class methods
##

def ValidPane(ch, extend=False): return True if (ch in PANE_CHARACTERS or (extend and ch in PANE_RESERVED)) else False
def ValidPanes(extend=False): return (PANE_CHARACTERS + PANE_RESERVED) if extend else PANE_CHARACTERS

##
## Windowgram Convert
##
## These are windowgram conversion macros as static methods
##

class Windowgram_Convert():

    ## String <-> Lines ... windowgram_lines == [ "12", "34", ... ]

    @staticmethod
    def String_To_Lines(windowgram):
        return [ linestrip(line) for line in list(filter(None, (windowgram+"\n").split("\n"))) ] # No blank lines
    @staticmethod
    def Lines_To_String(windowgram_lines):
        return "\n".join([ line for line in windowgram_lines ]) + "\n" # Each line has one \n

    ## String <-> Chars ... windowgram_chars == [ ['1', '2'], ['3', '4'], ... ]

    @staticmethod
    def String_To_Chars(windowgram):
        # A list of lists, each containing one or more single characters representing a line
        return [ [ ch for ch in list(ln) ] for ix, ln in enumerate(windowgram.split("\n")[:-1]) ]
    @staticmethod
    def Chars_To_String(windowgram_chars):
        return Windowgram_Convert.Lines_To_String( [ "".join(line_chars) for line_chars in windowgram_chars ] )

    ## String <-> Parsed ... windowgram_parsed == { 'Q': { 'n': 'Q', 'x': 1, 'y': 1, 'w': 1, 'h': 1  }, ... }

    @staticmethod
    def String_To_Parsed(windowgram, extend=False): # windowgram_parsed, error_string, error_line
        windowgram_lines = Windowgram_Convert.String_To_Lines(windowgram)
        windowgram_parsed = {}
        panes_y = 0 # Line number
        try:
            panes_x = panes_y = width = 0
            for ix, line in enumerate(windowgram_lines):
                if not line: continue
                panes_y += 1
                panes_x = 0
                for ch in line:
                    if not ValidPane(ch, extend):
                        raise Exception("Windowgram must contain valid identifiers: [0-9a-zA-Z]")
                if panes_y > 1 and len(line) != width:
                    raise Exception("Windowgram width does not match previous lines")
                else:
                    if width == 0: width = len(line)
                    for ch in line:
                        panes_x += 1
                        if not ValidPane(ch, extend):
                            raise Exception("Windowgram must contain valid identifiers: [0-9a-zA-Z]")
                        # Builds "bounding box" around pane for easy error detection through overlap algorithm
                        if not ch in windowgram_parsed:
                            # New pane
                            windowgram_parsed[ch] = { 'n': ch, 'x': panes_x, 'y': panes_y, 'w': 1, 'h': 1 }
                        else:
                            # Expand width
                            x2 = panes_x - windowgram_parsed[ch]['x'] + 1
                            if x2 > windowgram_parsed[ch]['w']:
                                windowgram_parsed[ch]['w'] = x2
                            # Expand height
                            y2 = panes_y - windowgram_parsed[ch]['y'] + 1
                            if y2 > windowgram_parsed[ch]['h']:
                                windowgram_parsed[ch]['h'] = y2
                            # Update x
                            if windowgram_parsed[ch]['x'] > panes_x:
                                windowgram_parsed[ch]['x'] = panes_x
            if not windowgram_parsed: raise Exception("Windowgram not specified")
        except Exception as error:
            return None, str(error), panes_y
        return windowgram_parsed, None, None
    @staticmethod
    def Parsed_To_String(windowgram_parsed): # windowgram_string
        # TODO: Probably should do error handling
        windowgram_list = []
        for paneid in windowgram_parsed.keys():
            pane = windowgram_parsed[paneid]
            for y in range( pane['y'], pane['y'] + pane['h'] ):
                for x in range( pane['x'], pane['x'] + pane['w'] ):
                    ix = int(x) - 1
                    iy = int(y) - 1
                    while len(windowgram_list) <= iy: windowgram_list.append([])
                    while len(windowgram_list[iy]) <= ix: windowgram_list[iy].append([])
                    windowgram_list[iy][ix] = pane['n']
        windowgram_string = ""
        for line in windowgram_list:
            windowgram_string += "".join(line) + "\n"
        return windowgram_string

    ## String <-> Mosaic ... windowgram_mosaic == ( wg_base, [ [ wg_data, wg_mask ], [ wg_data, wg_mask ], ... ] )

    @staticmethod
    def String_To_Mosaic():
        # This data is only generated by flex commands
        pass
    @staticmethod
    def Mosaic_To_String(windowgram_mosaic): # windowgram_string
        # From wg_base, merges pairs of [ wg_data, wg_mask ] onto it, ordered bottom to top
        wg_base, pairs = windowgram_mosaic
        s_l = wg_base.Export_Lines()    # Source
        for w, m in pairs:
            t_l = w.Export_Lines()      # Target
            m_l = m.Export_Lines()      # Mask
            w_l, s_l = s_l, []          # Work
            for iy in range(len(w_l)):
                line = ""
                for ix in range(len(w_l[iy])): line += w_l[iy][ix] if m_l[iy][ix] != MASKPANE_1 else t_l[iy][ix]
                s_l.append(line)
        return Windowgram_Convert.Lines_To_String( s_l )

    ## String -> Lines -> String ... Purifies the windowgram by stripping comments and whitespace

    @staticmethod
    def Purify(windowgram):
        # Full cycle purification -- asserts consistency of form
        return Windowgram_Convert.Lines_To_String( Windowgram_Convert.String_To_Lines( windowgram ) )

##
## Windowgram
##
## Error handling is done by polling GetErrorPair() after calling an error-generating method
##

class Windowgram():

    def __init__(self, windowgram_raw, extend=False):
        # Mask mode (extend parameter) should only be enabled here to avoid type uncertainty
        self.extend = extend # For masking
        self.change_count = 0
        self.change_query = 0
        self.Import_Raw(windowgram_raw)
        self.NoChange()

    def Reset(self):
        self.windowgram_string = None
        self.error_string = None
        self.error_line = 0
        self.change_count += 1

    def GetErrorPair(self): # Resets error when polled.  Returns: error_string, error_line
        error_string = self.error_string
        error_line = self.error_line
        self.error_string = None
        self.error_line = 0
        return error_string, error_line

    ##
    ## Imports
    ##

    def Import_Raw(self, windowgram_raw):
        self.Reset()
        self.windowgram_string = Windowgram_Convert.Purify( windowgram_raw ) # Strip comments and whitespace
        self.Changed()
    def Import_String(self, windowgram_string):
        return self.Import_Raw( windowgram_string )
    def Import_Lines(self, windowgram_lines):
        return self.Import_Raw( Windowgram_Convert.Lines_To_String(windowgram_lines) )
    def Import_Chars(self, windowgram_chars):
        return self.Import_Raw( Windowgram_Convert.Chars_To_String(windowgram_chars) )
    def Import_Parsed(self, windowgram_parsed):
        return self.Import_Raw( Windowgram_Convert.Parsed_To_String(windowgram_parsed) )
    def Import_Mosaic(self, windowgram_mosaic):
        return self.Import_Raw( Windowgram_Convert.Mosaic_To_String(windowgram_mosaic) )
    def Import_Wg(self, wg):
        return self.Import_Raw( wg.Export_String() )

    ##
    ## Exports ... The windowgram is only converted upon request
    ##

    def Export_String(self):
        return self.windowgram_string
    def Export_Lines(self):
        return Windowgram_Convert.String_To_Lines( self.windowgram_string )
    def Export_Chars(self):
        return Windowgram_Convert.String_To_Chars( self.windowgram_string )
    def Export_Parsed(self): # Generates error
        windowgram_parsed, error_string, error_line = \
            Windowgram_Convert.String_To_Parsed( self.windowgram_string, self.extend )
        if error_string:
            windowgram_parsed = {}
            self.error_string = error_string
            self.error_line = error_line
        return windowgram_parsed

    ##
    ## Analyze windowgram for metrics and supportability, performed on demand
    ##

    def Analyze_WidthHeight(self):
        windowgram_lines = Windowgram_Convert.String_To_Lines( self.windowgram_string )
        return [ (max([ len(line) for line in windowgram_lines ]) if windowgram_lines else 0), len( windowgram_lines ) ]
    def Analyze_IsBlank(self):
        return True if not max(self.Analyze_WidthHeight()) else False
    def Analyze_Layers(self):
        return 1 # Fixed for now
    def Analyze_Type(self, relative):
        # Determine compatibility (split, tiled, layered)
        analysis_type = ""
        while True:
            # Detect layered
            windowgram_parsed, error, _ = Windowgram_Convert.String_To_Parsed( self.windowgram_string )
            if error:
                analysis_type = "ERROR"
                break
            list_panes, windowgram_parsed = SortPanes( windowgram_parsed )
            overlap_pane1, overlap_pane2 = PaneOverlap( list_panes )
            if overlap_pane1 or overlap_pane2:
                analysis_type = "layered" # Implicit
                break
            # Detect split
            sw = { 'print': None, 'verbose': 0, 'relative': relative, 'scanline': False } # No print
            list_split, list_links = SplitProcessor( sw, self, 1024, 1024, list_panes ) # Avoid layout errors
            splityes = True
            for split in list_split:
                #
                # Readability
                #
                list_split_linkid = split['linkid']     # 1234          This is for cross-referencing
                ent_panes = ''
                for i in list_panes:
                    if 'l' in i and i['l'] == split['linkid']:
                        ent_panes = i
                        break
                if not ent_panes:
                    splityes = False
                    break
            if splityes:
                analysis_type = "split"
                break
            # Assume tiled
            analysis_type = "tiled"
            break
        return analysis_type

    ##
    ## Change Detection (has change_count been incremented since last query)
    ##

    def Changed(self): self.change_count += 1
    def NoChange(self): self.change_query = self.change_count
    def HasChanged_SenseOnly(self): return True if self.change_count == self.change_query else False
    def HasChanged(self): flag = self.HasChanged_SenseOnly() ; NoChange() ; return flag

    ##
    ## Pane / Panes
    ##

    def Panes_GetUsedUnused(self): # used, unused
        # Mutually exclusive list of pane ids for given windowgram
        windowgram_lines = Windowgram_Convert.String_To_Lines( self.windowgram_string )
        used = "".join( sorted( list(set(list("".join(windowgram_lines)))), 
            key=lambda x: ValidPanes(self.extend).find(x) ) )
        unused = "".join( [ paneid for paneid in ValidPanes(self.extend) if paneid not in used ] )
        return used, unused

    def Panes_GetNewPaneId(self, preferred=None): # newpaneid, error
        # Input preferred: None == First available pane / paneid == Specified if valid
        used, unused = self.Panes_GetUsedUnused()
        if not unused: return None, "All pane identifiers have been used"
        if preferred is None: return unused[0], None
        if preferred not in ValidPanes(self.extend): return None, "Invalid pane identifier"
        if preferred not in unused: return None, "Pane id `" + preferred + "` is in use"
        return preferred, None

    def Panes_HasPane(self, pane):
        for line in Windowgram_Convert.String_To_Lines( self.windowgram_string ):
            for ch in line:
                if ch == pane: return True
        return False

    def Panes_PaneXYXY(self, pane): # x1, y1, x2, y2
        if not self.Panes_HasPane( pane ): return 0, 0, 0, 0
        windowgram_lines = Windowgram_Convert.String_To_Lines( self.windowgram_string )
        x2 = y2 = -1
        x1 = len(windowgram_lines[0])
        y1 = len(windowgram_lines)
        for y, line in enumerate(windowgram_lines):
            for x, char in enumerate(line):
                if char == pane:
                    if x < x1: x1 = x
                    if x > x2: x2 = x
                    if y < y1: y1 = y
                    if y > y2: y2 = y
        return x1+1, y1+1, x2+1, y2+1

    def Panes_PaneXYWH(self, pane): # x, y, w, h
        if not self.Panes_HasPane( pane ): return 0, 0, 0, 0
        x1, y1, x2, y2 = self.Panes_PaneXYXY( pane )
        return x1, y1, x2-x1+1, y2-y1+1

    def Panes_Renamer(self, panes, pane):
        # Supports multiple panes renaming, use only when you know the results will be valid
        new_lines = []
        for line in Windowgram_Convert.String_To_Lines( self.windowgram_string ):
            new_lines.append( "".join( [ (ch if ch not in panes else pane) for ch in line ] ) )
        self.Import_Lines( new_lines )

##
## Windowgram Masking Functions
##

def Windowgram_Mask_Generate(wg, panes): # wg_mask
    # Returns a windowgram with non-standard panes for use with masking: "." for zero, ":" for one
    windowgram_parsed = wg.Export_Parsed()
    width, height = wg.Analyze_WidthHeight()
    # Produce mask
    mask_windowgram_chars = []
    while len(mask_windowgram_chars) < height: mask_windowgram_chars.append( list(MASKPANE_0 * width) )
    for key in list(panes):
        pane = windowgram_parsed[key]
        for y in range( pane['y'], pane['y'] + pane['h'] ):
            for x in range( pane['x'], pane['x'] + pane['w'] ):
                mask_windowgram_chars[y-1][x-1] = MASKPANE_1
    # Return mask as wg instance
    wg_mask = Windowgram("", True) # Create a windowgram for masking
    wg_mask.Import_Chars( mask_windowgram_chars )
    return wg_mask

##
## Pane List Functions
##

def PaneList_DiffLost(this, that): # lostpanes
    # Parameters are Windowgram instances, aka wg
    used1, _ = this.Panes_GetUsedUnused()
    used2, _ = that.Panes_GetUsedUnused()
    lostpanes, _ = Windowgram( "".join( list(set(used1) - set(used2)) ) ).Panes_GetUsedUnused()
    return lostpanes

def PaneList_MovePanes(list1, list2, panes): # newlist1, newlist2
    # Moves specified batch of panes (if present) from "list1" into "list2" ... Returns new lists in that order
    for pane in list(panes):
        if pane in ValidPanes() and (pane in list1 or pane not in list2):
            # Assert ordering every pass, as in some situations the panes will be unsorted
            list1 = "".join([ch for ch in ValidPanes() if ch in list1 and ch != pane])
            list2 = "".join([ch for ch in ValidPanes() if ch in list2 or ch == pane])
    return list1, list2

def PaneList_AssimilatedSorted(this, that): # this_plus_that_assimilated_and_sorted
    return "".join( sorted( set( this + that ), key=lambda x: ValidPanes().find(x) ) )



##----------------------------------------------------------------------------------------------------------------------
##
## Session file objects
##
##----------------------------------------------------------------------------------------------------------------------

##
## Window declaration macros
## A window declaration without a specified name is not allowed, except during the file parsing
##

is_windowdeclaration = lambda line: re.search(r"window", line)
windowdeclaration_name = lambda line: " ".join(re.split(r"[ \t]+", line)[1:]) if is_windowdeclaration(line) else ""

##
## Session declaration macros
##

is_sessiondeclaration = lambda line: re.search(r"session", line)
sessiondeclaration_name = lambda line: " ".join(re.split(r"[ \t]+", line)[1:]) if is_sessiondeclaration(line) else ""

##
## Parsed session file classes
##

class BatchOfLines(object): # A batch of lines (delimited string) with the corresponding line numbers (int list)
    def __init__(self):
        self.lines = ""             # Lines delimited by \n, expects this on the last line in each batch of lines
        self.counts = []            # For each line in lines, an integer representing the corresponding line number
    def __repr__(self): # Debugging
        return "lines = \"" + self.lines.replace("\n", "\\n") + "\", counts = " + repr(self.counts)
    def AppendBatch(self, lines, start, increment=True):
        linecount = len(lines.split("\n")[:-1]) # Account for extra line
        self.lines += lines
        self.counts += [line for line in range(1, linecount+1)] if increment else ([start] * linecount)
    def IsEmpty(self):
        return True if not self.lines else False

class Window(object): # Common container of window data, divided into sections identified by the keys below
    def __init__(self):
        self.__dict__['data'] = {} # { 'title_comments': string_of_lines, 'title': string_of_lines, ... }
        self.__dict__['line'] = {} # { 'title_comments': first_line_number, 'title': first_line_number, ... }
        for key in self.ValidKeys(): self.ClearKey(key) # Clear all keys
    def __getitem__(self, key): # Invalid keys always return ""
        return self.__dict__['data'][key] if key in self.ValidKeys() else ""
    def __setitem__(self, key, value): # Invalid keys quietly dropped
        if key in self.ValidKeys(): self.__dict__['data'][key] = value
    def __repr__(self): # Debugging
        return "\n__repr__ = [\n" + \
            ", ".join(
                [ "'" + key + "': [ data = \"" + self.__dict__['data'][key].replace("\n", "\\n") + \
                "\", starting_line_number = " + str(self.__dict__['line'][key]) + " ]\n" \
                for key in self.ValidKeys() if self[key] is not "" ] \
            ) + \
        " ]\n"
    def ClearKey(self, key):
        if key in self.ValidKeys():
            self.__dict__['data'][key] = ""
            self.__dict__['line'][key] = 0
    def ValidKeys(self): # Ordered by appearance
        return "title_comments title windowgram_comments windowgram directions_comments directions".split(" ")
    def Serialize(self): # Serialized by appearance
        return "".join( [ self[key] for key in self.ValidKeys() ] )
    def WorkingKeys(self):
        return [ key for key in self.ValidKeys() if self[key] is not "" ]
    def IsFooter(self):
        summary = " ".join( self.WorkingKeys() )
        return True if summary == "title_comments" or summary == "" else False
    def FirstLine(self, key):
        return True if key in self.ValidKeys() and self.__dict__['line'][key] == 0 else False
    def SetLine(self, key, line):
        if key in self.ValidKeys(): self.__dict__['line'][key] = line
    def GetLine(self, key):
        return self.__dict__['line'][key] if key in self.ValidKeys() else 0
    def SetIfNotSet(self, key, line):
        if self.FirstLine(key): self.SetLine(key, line)
    def GetLines(self, key):
        return self.__dict__['line'][key]
    def SplitCleanByKey(self, key):
        return [ line[:line.index('#')].strip() if '#' in line else line.strip() for line in self[key].split("\n") ]

class SessionFile(object):
    def __init__(self, filename):
        self.filename = filename
        self.Clear()
        self.modified = False   # Explicit modification
    def Clear(self):
        self.format = None      # "shorthand" or "yaml"
        self.footer = ""        # footer comments
        self.windows = []       # [ window, window, ... ]
    def Load_Shorthand_SharedCore(self, bol):
        # Actually locals
        self.state = 0
        self.window = None
        self.line = [ None, None ]      # line without cr, line number
        self.comments = [ "", None ]    # lines with cr, first line number
        # Switchboard
        switchboard = [
            "title_comments",       # state == 0 <- loop to / file footer saved here in its own window
            "title",                # state == 1
            "windowgram_comments",  # state == 2
            "windowgram",           # state == 3
            "directions_comments",  # state == 4
            "directions",           # state == 5
            "UNUSED_comments",      # state == 6 <- loop from / always appends this to "title_comments"
        ]
        # Iterate lines and append onto respective window keys
        lines = bol.lines.split("\n")[:-1] # Account for extra line
        lines_index = 0
        while True:
            def transfercomments(): # Transfer comments (if any) to the current window block
                if self.comments[0] is not None:
                    self.window[ switchboard[self.state] ] += self.comments[0]
                    self.window.SetIfNotSet( switchboard[self.state], self.comments[1] )
                self.comments[0] = self.comments[1] = None
            def nextwindow(): # This is called in two cases: 1) window declaration found, 2) end of file reached
                if self.window: self.windows.append( self.window )
                self.window = Window() ; self.state = 0 ; transfercomments() ; self.state = 1
            def addline(): # Adds current line to current block or comments
                if switchboard[self.state].endswith("_comments"): # Add to comments
                    if self.comments[0] is None: self.comments[0] = self.line[0] + "\n"
                    else: self.comments[0] += self.line[0] + "\n"
                    self.comments[1] = self.line[1] if self.comments[1] is None else self.comments[1]
                else: # Add to block
                    self.window[ switchboard[self.state] ] += self.line[0] + "\n"
                    self.window.SetIfNotSet( switchboard[self.state], self.line[1] )
                self.line[0] = self.line[1] = None # Ready to load next line
            # Load line with corresponding line number
            if self.line[0] is None and lines_index < len(lines): # Line
                self.line[0] = lines[lines_index] ; self.line[1] = bol.counts[lines_index]
                lines_index += 1
            if self.line[0] is None: # EOF
                # Hold comments so the footer doesn't get lost to the non-existent state 6 block
                hold = [ None, None ]
                hold[0], hold[1] = self.comments[0], self.comments[1]
                self.comments[0], self.comments[1] = None, None
                nextwindow()
                # Restore comments so they are assimilated as a proper footer
                self.comments[0], self.comments[1] = hold[0], hold[1]
                if self.comments[0] is not None:
                    self.state = 0
                    transfercomments()
                    nextwindow()
                # Done parsing
                break
            # Line used for analysis is stripped of all comments and whitespace
            lineused = self.line[0].strip()
            if lineused.find("#") >= 0: lineused = lineused[:lineused.find("#")].strip()
            # Append this line to section or comments
            if is_windowdeclaration(lineused): nextwindow() ; addline() ; self.state = 2 # New window declaration
            elif ( self.state == 2 or self.state == 4 ) and lineused: transfercomments() ; self.state += 1 ; addline()
            elif ( self.state == 3 or self.state == 5 ) and not lineused: self.state += 1 ; addline()
            elif self.state == 6 and lineused: addline() ; self.state = 5 ; transfercomments() # Back up and add to 5
            else: addline() # Everything else adds the line / Until first window declaration is found add to comments
        # Any comments at end of file should be extracted into the footer string
        if len(self.windows) and self.windows[len(self.windows)-1].IsFooter():
            window = self.windows.pop(len(self.windows)-1)
            self.footer = window.Serialize()
    def Load_Shorthand(self, rawfile):
        self.Clear()
        self.format = "shorthand"
        bol = BatchOfLines()
        bol.AppendBatch( rawfile, 1 )
        self.Load_Shorthand_SharedCore( bol )
    def Load_Yaml(self, rawfile):
        self.Clear()
        self.format = "yaml"
        # Yaml -> Dict
        try:
            # Line numbers (per window) with pyyaml from: https://stackoverflow.com/a/13319530
            loader = yaml.SafeLoader(rawfile)
            def compose_node(parent, index):
                line = loader.line # The line number where the previous token has ended (plus empty lines)
                node = yaml.SafeLoader.compose_node(loader, parent, index)
                node.__line__ = line + 1
                return node
            def construct_mapping(node, deep=False):
                mapping = yaml.SafeLoader.construct_mapping(loader, node, deep=deep)
                mapping['__line__'] = node.__line__
                return mapping
            loader.compose_node = compose_node
            loader.construct_mapping = construct_mapping
            # Load into dict, now with line numbers for location of window in YAML
            filedict = loader.get_single_data() # filedict = yaml.safe_load( rawfile ) # Without line numbers
        except:
            filedict = {}
        # Dict -> Shorthand
        group_session = []
        group_other = []
        bol = BatchOfLines()
        bol.AppendBatch( "\n", 0, False ) # Translated YAML -> Shorthand, no need for header
        if type(filedict) is list:
            for entry in filedict:
                # Session renames
                if type(entry) is dict and 'session' in entry:
                    linenumber = entry['__line__'] if '__line__' in entry else 0
                    rawfile_shorthand = "session " + str(entry['session']) + "\n\n"
                    group_session.append( [ rawfile_shorthand, linenumber, False ] )
                # Name blocks... Windows are identified by 'name' key
                elif type(entry) is dict and 'name' in entry:
                    # Must contain 'windowgram' and 'directions' as block literals
                    windowgram = entry['windowgram'] if 'windowgram' in entry else ""
                    directions = entry['directions'] if 'directions' in entry else ""
                    linenumber = entry['__line__'] if '__line__' in entry else 0
                    rawfile_shorthand = \
                        "window " + str(entry['name']) + "\n\n" + windowgram + "\n" + directions + "\n\n\n"
                    group_other.append( [ rawfile_shorthand, linenumber, False ] )
        # Append data, if any; this will force session renames to the top of the shorthand file
        if group_session or group_other:
            # Session renaming is only valid at top of file
            for rawfile_shorthand, linenumber, flag in group_session:
                bol.AppendBatch( rawfile_shorthand, linenumber, False )
            # Everything else follows
            for rawfile_shorthand, linenumber, flag in group_other:
                bol.AppendBatch( rawfile_shorthand, linenumber, False )
        # Shorthand -> Core
        self.Load_Shorthand_SharedCore( bol )
    def Load(self):
        # Load raw data
        rawfile = ""
        f = open(self.filename, "rU")
        while True:
            line = f.readline()
            if not line: break # EOF
            rawfile += line
        # Detect file format
        format_yaml = False
        for line in rawfile.split("\n"):
            if line.find("#") >= 0: line = line[:line.find("#")]
            line = line.strip()
            if line:
                if line[0] == "-":
                    format_yaml = True
                break
        # Parse the file
        if format_yaml:
            if not INSTALLED_PYYAML:
                print("You have specified a session file in YAML format, yet you do not have pyyaml installed.")
                print("Install pyyaml first, usually with a command like: `sudo pip-python3 install pyyaml`")
                exit(0)
            self.Load_Yaml( rawfile )
        else:
            self.Load_Shorthand( rawfile )
    def Save(self):
        self.modified = False
        if self.filename and self.format:
            if self.format == "shorthand":
                # Shorthand
                f = open(self.filename, 'w')
                for window in self.windows: f.write( window.Serialize() )
                f.write( self.footer )
            if self.format == "yaml":
                # YAML
                formatted = "##\n## YAML session file generated by tmuxomatic flex " + VERSION + "\n##\n\n---\n\n"
                # Required for writing block literals, source: https://stackoverflow.com/a/6432605
                def change_style(style, representer):
                    def new_representer(dumper, data):
                        scalar = representer(dumper, data)
                        scalar.style = style
                        return scalar
                    return new_representer
                class literal_str(str): pass
                represent_literal_str = change_style('|', yaml.representer.SafeRepresenter.represent_str)
                yaml.add_representer(literal_str, represent_literal_str)
                # Add the session name change
                rename = self.RenameIfSpecified_Raw()
                if rename is not None:
                    formatted += yaml.dump( [{'session': rename}], \
                        indent=2, default_flow_style=False, explicit_start=False )
                    formatted += "\n"
                # Now add all windows to a dictionary for saving
                for ix, window in enumerate(self.windows):
                    serial = 1+ix
                    # Extract name: "window panel 1\n" -> "panel 1"
                    name = windowdeclaration_name( self.Get_WindowDeclarationLine( serial ) )
                    # Append window definition
                    # TODO: Sort as "name", "windowgram", "directions".  Maybe use: http://pyyaml.org/ticket/29
                    window_dict = {
                        'name': str(name),
                        'windowgram': literal_str(window['windowgram']),
                        'directions': literal_str(window['directions']),
                    }
                    # Dump to string, with linebreaks
                    formatted += yaml.dump( [window_dict], indent=2, default_flow_style=False, explicit_start=False )
                    formatted += "\n"
                # Write file
                f = open(self.filename, 'w')
                f.write( formatted )
    def Ascertain_Trailing_Padding(self, string):
        count = 0
        for ix in range( len(string)-1, -1, -1 ):
            if string[ix] == "\n": count += 1
            else: break
        return count
    def Duplicate_Trailing_Padding(self, string, minimum):
        count = self.Ascertain_Trailing_Padding(string)
        if count < minimum: count = minimum
        return "\n" * count
    def Replace_TitleComments(self, serial, comments):
        if serial < 1 or serial > self.Count_Windows(): return
        padding = self.Duplicate_Trailing_Padding(self.windows[serial-1]['title_comments'], 1)
        self.windows[serial-1]['title_comments'] = comments + padding
        self.modified = True
    def Replace_Title(self, serial, name):
        if serial < 1 or serial > self.Count_Windows(): return
        padding = self.Duplicate_Trailing_Padding(self.windows[serial-1]['title'], 1)
        self.windows[serial-1]['title'] = "window " + name + padding
        self.modified = True
    def Replace_Windowgram(self, serial, windowgram_string): # TODO: Replace by wg
        if serial < 1 or serial > self.Count_Windows(): return
        self.windows[serial-1]['windowgram'] = Windowgram( windowgram_string ).Export_String() # Clean via class
        self.modified = True
    def Modified(self): # See flag use for limitations
        return self.modified
    def Count_Windows(self):
        return len(self.windows)
    def Serial_Is_Valid(self, serial):
        return serial >= 1 and serial <= len(self.windows)
    def Get_WindowDeclarationLine(self, serial):
        if serial < 1 or serial > self.Count_Windows(): return "???" # Out of range
        return linestrip(self.windows[serial-1]['title'].split("\n")[0]) # Window declaration is on first line
    def Get_Name(self, serial):
        if serial < 1 or serial > self.Count_Windows(): return "???" # Out of range
        return windowdeclaration_name( self.Get_WindowDeclarationLine( serial ) )
    def Get_WindowgramDimensions_Int(self, serial):
        windowgram_string = self.windows[serial-1]['windowgram']
        return Windowgram(windowgram_string).Analyze_WidthHeight()
    def Get_Windowgram(self, serial): # windowgram_string
        if serial < 1 or serial > self.Count_Windows():
            if warning is None: return None
            return None, "Out of range"
        windowgram_string = Windowgram_Convert.Purify(self.windows[serial-1]['windowgram'])
        return windowgram_string
    def Get_Wg(self, serial): # wg
        windowgram_string = self.Get_Windowgram(serial)
        return Windowgram(windowgram_string) if windowgram_string else None
    def Add_Windowgram(self, comments, name, windowgram_string):
        self.windows.append( Window() )
        serial = len(self.windows)
        # Transfer footer to title comments for new window
        while len(self.footer) > 1 and not self.footer.endswith("\n\n"): self.footer += "\n"
        if not self.footer: self.footer = "\n"
        self.windows[serial-1]['title_comments'] = self.footer
        self.footer = ""
        # Build window
        self.windows[serial-1]['title_comments'] += comments if comments[-1:] == "\n" else comments + "\n"
        name = "window " + name # Make a declaration
        self.windows[serial-1]['title'] = name if name[-1:] == "\n" else name + "\n"
        self.windows[serial-1]['windowgram_comments'] = "\n"
        self.windows[serial-1]['windowgram'] = \
            windowgram_string if windowgram_string[-1:] == "\n" else windowgram_string + "\n"
        # Modified
        self.modified = True
        return serial
    def RenameIfSpecified_Raw(self): # new_name (raw) or None
        # Parse every line and change the name if specified (session rename only valid in comments sections)
        new_name = None
        if self.windows:
            batch = self.windows[0].SplitCleanByKey('title_comments')
            for line in batch:
                if is_sessiondeclaration(line):
                    new_name = sessiondeclaration_name(line)
        return new_name
    def RenameIfSpecified(self): # new_name (modified) or None
        new_name = self.RenameIfSpecified_Raw()
        return None if new_name is None else (PROGRAM_THIS + "_" + new_name)



##----------------------------------------------------------------------------------------------------------------------
##
## Flex cores
##
## These functions are shared by multiple flex commands.
##
##----------------------------------------------------------------------------------------------------------------------

##
## Scale core ... Scales a windowgram
##
## Used by ... scale, break
##

def scalecore_v1(windowgram_string, w_chars, h_chars):
    ##
    ## Based on the scale code used in tmuxomatic 1.x
    ##
    def scale_one(element, multiplier):
        # Scale element using integer rounding, multiplier must be float
        q, r = math.modf( float(element - 1) * multiplier )
        if q >= .5: r += 1
        return int(r) + 1
    def scale_windowgram(list_panes, ax, ay): # lost_count
        # Scales the windowgram
        lost = 0
        for paneid in list_panes.keys():
            pane = list_panes[paneid]
            # The following were conditional prior to 2.4, removed to allow scale to 0 since it's handled by caller
            pane['w'] = scale_one( pane['x'] + pane['w'], ax )
            pane['h'] = scale_one( pane['y'] + pane['h'], ay )
            pane['x'] = scale_one( pane['x'], ax )
            pane['y'] = scale_one( pane['y'], ay )
            pane['w'] -= pane['x']
            pane['h'] -= pane['y']
            if not pane['x'] or not pane['y'] or not pane['w'] or not pane['h']: lost += 1
        return lost
    # Get pane list
    list_panes = Windowgram(windowgram_string).Export_Parsed()
    # Set the multipliers
    ww, wh = Windowgram(windowgram_string).Analyze_WidthHeight()
    ax, ay = float(w_chars) / float(ww), float(h_chars) / float(wh)
    # Perform the scale
    list_panes_scaled = copy.deepcopy( list_panes )
    scale_windowgram( list_panes_scaled, ax, ay )
    windowgram_string_new = Windowgram_Convert.Parsed_To_String( list_panes_scaled )
    return windowgram_string_new

def scalecore_v2(windowgram, w_chars, h_chars):
    ##
    ## Simpler but less accurate scale code added in tmuxomatic 2.0
    ##
    from_w, from_h = Windowgram(windowgram).Analyze_WidthHeight()
    x_mul = float(w_chars) / float(from_w)
    y_mul = float(h_chars) / float(from_h)
    windowgram_chars = Windowgram_Convert.String_To_Chars(windowgram)
    windowgram_chars_scaled = []
    for y in range(0, h_chars):
        windowgram_chars_scaled.append( [ windowgram_chars[ int(y/y_mul) ][ int(x/x_mul) ] \
            for x in range(0, w_chars) ] )
    windowgram_new = Windowgram_Convert.Chars_To_String( windowgram_chars_scaled )
    return windowgram_new

def scalecore(windowgram, w_chars, h_chars, retry=None): # TODO: Scale by wg to remove the Windowgram_Convert usage
    ##
    ## Main entry for all scale functions
    ##
    windowgram_scaled = "" # Scope, and reset in case of error
    # Retry with necessary increment and/or decrement until desired pane dimensions are reached.  This is required for
    # commands like "break", which need to scale to a specific pane size.  There's likely a way to derive these metrics
    # reliably, but this works too.  Verify that two resizes are necessary with the following commands:
    #       "new 1 ; scale 42x42 ; break 1 6x6 ; break 1 3x3"
    tries = 0
    tries_max = 16 # An infinite loop is unlikely, but this maximum will prevent such an occurrence
    paneid = exp_w = exp_h = None
    if retry and type(retry) is tuple and len(retry) == 3:
        paneid, exp_w, exp_h = retry # retry == ( paneid, w, h )
        if Windowgram( windowgram ).Panes_HasPane( paneid ): tries = tries_max
        else: paneid = None
    # Scale until satisfied; this loop is for pane measurement, since the windowgram should always scale on first try.
    if tries < 1: tries = 1
    try_w, try_h = w_chars, h_chars
    while tries:
        # Scale core discrepancy example, note that v2 loses 3 panes, but v1 does not:
        #       "new 1 ; break 1 2x2 ; scale 3x3 ; scale 2x2"
        windowgram_scaled = scalecore_v1( windowgram, try_w, try_h ) # Using v1 as of 2.3
        if paneid:
            _, _, new_w, new_h = Windowgram( windowgram_scaled ).Panes_PaneXYWH( paneid )
            if new_w == exp_w and new_h == exp_h: break
            try_w += 1 if new_w < exp_w else -1 if new_w > exp_w else 0
            try_h += 1 if new_h < exp_h else -1 if new_h > exp_h else 0
        tries -= 1
    return windowgram_scaled

##
## Group core ... Tests group of panes for contiguity, returns group capability, if panes are missing it suggests them
##
## Used by ... join
## Anticipating ... drag, insert, delete, flip (group), mirror (group)
##

class GroupStatus:
    Success = 1
    Invalid_Panes = 2
    Insufficient_Panes = 3

def groupcore(wg, panes): # flag_groupstatus, string_suggestions
    ##
    ## Groups the specified panes and returns the findings.  If the panes are valid, but there are gaps in the group,
    ## it recursively detects which panes need to be added to complete the group.  If a group is determined to be valid,
    ## the windowgram may be trivially updated by the user using a simple search and replace.
    ##
    used, unused = wg.Panes_GetUsedUnused()
    # Pane validity
    for pane in set(panes):
        if pane not in used or pane in unused:
            return GroupStatus.Invalid_Panes, None
    # Function for assembly of panes detected within any gaps of the mask
    def pane_deficit_detection(wg_win, x1, y1, x2, y2, panes):
        # Parameters: windowgram, rectangular bounds of mask, valid panes
        deficient_panes = ""
        wgw_windowgram_chars = wg_win.Export_Chars()
        wgm_windowgram_chars = wg_msk.Export_Chars()
        for y in range( len(wgw_windowgram_chars) ):
            for x in range( len(wgw_windowgram_chars[y]) ):
                w, m = wgw_windowgram_chars[y][x], wgm_windowgram_chars[y][x]
                if x >= x1-1 and x <= x2-1 and y >= y1-1 and y <= y2-1 and w not in set(panes):
                    deficient_panes += w
        return deficient_panes
    # Run deficit detection until none remain (e.g., mask == windowgram)
    suggestions = ""
    while True:
        # Draw mask and yield rectangular bounds
        wg_msk = Windowgram_Mask_Generate( wg, panes )
        x1, y1, x2, y2 = wg_msk.Panes_PaneXYXY( MASKPANE_1 )
        # Find pane content of any existing gaps
        deficient_panes = pane_deficit_detection( wg, x1, y1, x2, y2, panes )
        if not deficient_panes: break
        panes = PaneList_AssimilatedSorted( panes, deficient_panes )
        suggestions = PaneList_AssimilatedSorted( suggestions, deficient_panes )
    # Result by now will be either of these
    if not suggestions: return GroupStatus.Success, ""
    return GroupStatus.Insufficient_Panes, suggestions



##----------------------------------------------------------------------------------------------------------------------
##
## Flex (windowgram modification console)
##
##----------------------------------------------------------------------------------------------------------------------
##
## Planned modifiers:
##
##          When dragging an edge, it will be forced to stop for pane preservation
##          When dragging a group edge, the internal edges are scaled, only the group edge is contiguous
##          Drags specified edges, keeps opposing edges pinned, and scales the inner edges
##          May need a specialized scaler for this command
##          Maximum scale range depends whether a pane disappears or not
##          Dragging pushing edges was considered, but this would get messy and probably unnecessary
##
##      drag <panes> <dir> <how>                    drags edge, panes == xyz / dir == up / how == 50%
##      drag <edge> <panes> <dir> <how>             drags group edge, edge == top, bottom, left, right
##
##          Modifiers insert and clone need to differentiate between a deduced edge (1 parameter), a specified edge (2),
##          and the cardinal edge of a specified group (2).  Each of these is handled by one master function that will
##          infer the intent by the specified arguments and their originating function.  This may even allow some degree
##          of reordering of arguments, e.g., axis-edge and direction-group.  Also maybe support as edge:axis and
##          group:direction, this would assist the highlighter when it's implemented.
##
##          Both insert and clone uses the [axis] parameter as quasi-optional.  If the edge is ambiguous, it requests it
##          for clarification.
##
##          Both insert and clone requires the edge-group parameter to have holes, all that is important the specified
##          edge and that it is unambiguous.
##
##          Already supported mid-stream optional arguments, to use from flex function, specify "axis_OPTIONAL".  Note
##          that there will still need to be two distinct functions, but they will both be wrappers for a core function.
##
##      insert [axis] <edge> <size> [newpanes]      insert pane at edge of panes, just like add but with panes
##      insert <direction> <group> <size> [newpanes]
##
##          The clone command takes the first group of panes (forming a full rectangle), and along the specified edge,
##          it stretches (like scale) the surrounding windowgram to accommodate, and inserts it in.  Most useful for
##          rapidly expanding common windowgram patters.
##
##          The [newpanes] argument follows the same order as the first <group> parameter.
##
##      clone <group> [axis] <edge> [newpanes]
##      clone <group> <direction> <group> [newpanes]
##
##          Other commands
##
##      delete <pane>                               remove pane from edge of window (del, clip, remove, drop, rm)
##      mirror <group>                              mirrors a group, supports *
##      flip <group>                                flips a group, supports *
##      rotate <how>                                how == cw, ccw, 180, interpret 1..3 and -1..-3 as multiples of 90
##
## Planned other:
##
##      again                                       repeat last command (flex recognized, not official)
##      undo                                        stack: undo command
##      redo                                        stack: redo command
##      wipe                                        stack: discard the windowgram modification history (cannot undo)
##      clip                                        stack: discard any commands that had been undone (cannot undo)
##
## Possible:
##
##      links                                       show list of directions
##      link [data...]                              add line to directions
##      unlink <line>                               remove from directions by line number
##      mvlink <line_from> <line_to>                move line in directions
##      breakout <pane> [shapes]                    break with axial concatenated shapes == 2x2; x 2x2 3x1; y 1 3x3 1
##      shuffle <panegroup1> <panegroup2>           shuffle if all bounding boxes share full edge, or are of equal size
##      clonewindow <newname>                       copy current selected window into a new window and select
##      move <panes1> <panes2>                      swap if both panes are defined otherwise rename (probably redundant)
##      blockswap <panes1> <panes2>                 swaps one block of panes for another, e.g. `BLDbld` with `1` in demo
##
## Expectations:
##
##      The object (pane, group, edge) should always be the first argument to any command (with exception for qualifier)
##
##      Any modification of the windowgram outside of flex will result in a "manual" entry in flex stack
##
##      All ordering is in English order: front -> back, top -> bottom, left -> right
##
## Stack Sketch:
##
##      new                 base
##      scale               base < scale
## ...  mirror              base   scale   scale   break   scale < mirror
## ...  undo                base   scale < scale > break   scale   mirror
##      redo                base   scale   scale < break > scale   mirror
## ...  undo                base < scale > scale   break   scale   mirror
##      break               base   scale < break
## ...  undo                base > scale   break
##      clear               base
##
##      The current element on stack should include arguments, all others show only the command
##
## Stack Storage:
##
##      @ FLEX HISTORY : Used by --flex shell, use flex command "clear" to remove, or manually remove these lines
##      @ aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
##      @ aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
##      @ aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
##      @ aaaaaaaaaaaaaaaaaaaaaaaaaa
##
##      Data has initial windowgram, current stack pointer, easily allows any step to be reproduced on demand
##      Data also has version, length, data checksum, current windowgram checksum for detecting manual edits
##      Data is stored between window header and the windowgram as compressed JSON + utf-8 encoded in base64
##      Overwrites entire session file with updated history block for every windowgram modification
##
## Console will be simple text, possibly use ncurses or urwid if it's present (installation is optional like yaml)
## Aliases for commands: "u" = undo.  Include control keys if possible: ^Z = undo, ^Y = redo, ^U = clear, ^D = exit
## Print warnings if common divisors could not be found (within a reasonable range, say up to 120 characters)
## Display / print: clear, windowgram, gap, warnings, stack, gap, menu, gap, prompt
##
##----------------------------------------------------------------------------------------------------------------------

describe = lambda kwargs: True if 'menu' in kwargs and kwargs['menu'] is True else False
usage_triplets = lambda cmd_dict: [ cmd_dict['usage'][ix:ix+3] for ix in range( 0, len(cmd_dict['usage']), 3 ) ]

##
## Output controls ... Only flex helpers and selectors should use this directly, others should use warnings queue
##

class FlexNotice(object):
    def __init__(self, level, message): self.level = level ; self.message = message
    def GetLvl(self): return self.level
    def GetMsg(self): return self.message

class FlexWarning(FlexNotice):
    def __init__(self, message): super( FlexWarning, self ).__init__( 0, message )

class FlexError(FlexNotice):
    def __init__(self, message): super( FlexError, self ).__init__( 1, message )

##
## Lists of commands ... Commands are ordered by appearance in source
##

flexmenu = []                       # List of all commands and aliases (recognition)
flexmenu_aliases = []               # List of all aliases (recognized not displayed)
flexmenu_list = []                  # List of primary commands (displayed at prompt)
flexmenu_grouped = {}               # List of grouped commands (for the short menus)

##
## Other globals
##

flexmenu_session = None             # Session object in global scope for modification by commands
flexmenu_index = [ 0 ]              # Selected window, list is for reference purposes only
flexsense = {
    'finished': False,              # User exit
    'restore': False,               # User exit: Restore original
    'execute': False,               # User exit: Run session
    'output': [],                   # Command output
    'notices': [],                  # Command notices: Print and continue (FlexWarning, FlexError)
    'errors': [],                   # Command errors: Print and exit
}
flexsense_reset = copy.deepcopy( flexsense )

##
## Flex: Conversion of windowgram metrics
## Supports floating point values (example: "2.5x")
##

def arg_is_multiplier(arg):
    if type(arg) is str:
        if arg[:-1] == "".join([ch for ch in arg[:-1] if ch in "0123456789.,"]): # Fixed float support
            if arg[-1:] == "x" or arg[-1:] == "X" or arg[-1:] == "*": return True
    return False

def arg_is_percentage(arg):
    if type(arg) is str:
        if arg[:-1] == "".join([ch for ch in arg[:-1] if ch in "0123456789.,"]): # Fixed float support
            if arg[-1:] == "%": return True
    return False

def arg_is_characters(arg):
    try:
        _ = int(arg)
        return True
    except ValueError:
        return False

def size_GetType(arg):
    # Return type or None if invalid
    if arg_is_multiplier(arg): return "multiplier"
    if arg_is_percentage(arg): return "percentage"
    if arg_is_characters(arg): return "characters"
    return None

def size_GreaterOrEqualToBaseCharacters(arg, base_characters):
    # If the parameter is greater or equal to 100%, 1x, or base_characters
    if size_GetType(arg) is not None:
        if arg_is_multiplier(arg): return True if float(arg[:-1]) >= 1.0 else False
        if arg_is_percentage(arg): return True if float(arg[:-1]) >= 100.0 else False
        if arg_is_characters(arg): return True if int(arg) >= base_characters else False
    return None

def size_ConvertToCharacters(arg, base_characters):
    if size_GetType(arg) is not None:
        if arg_is_multiplier(arg): return int(float(base_characters) * float(arg[:-1]))
        if arg_is_percentage(arg): return int(float(base_characters) * (float(arg[:-1]) / 100.0))
        if arg_is_characters(arg): return int(arg)
    return None

##
## Flex: Expressions ... See actual usage for examples
##

## Directions

valid_directions = [ # These directions are recognized, the list is ordered 0123 == TBRL || NSEW
    [ "top", "t", "tp",     "north", "n",   "up", "u", "over", "above",     ],  # ix == 0 -> Vertical +
    [ "bottom", "b", "bt",  "south", "s",   "down", "d", "under", "below",  ],  # ix == 1 -> Vertical -
    [ "right", "r", "rt",   "east", "e"                                     ],  # ix == 2 -> Horizontal -
    [ "left", "l", "lt",    "west", "w"                                     ],  # ix == 3 -> Horizontal +
]

def direction_to_axiswithflag(direction): # axis_as_vh, negate_flag | None, None
    for ix, directions_ent in enumerate(valid_directions):
        if True in [True if d.lower().strip() == direction.lower().strip() else False for d in directions_ent]:
            if ix == 0: return "v", False   # Top
            if ix == 1: return "v", True    # Bottom
            if ix == 2: return "h", True    # Right
            if ix == 3: return "h", False   # Left
    return None, None

## Detections

is_axis_vert = lambda axis: True if axis in [ "v", "vertical", "vert" ] else False
is_axis_horz = lambda axis: True if axis in [ "h", "horizontal", "horz" ] else False

##
## Flex: Handling of newpanes parameter
##

def newpanes_RebuildPaneListsInPreferentialOrder(used, unused, newpanes):
    # Identify last valid pane in list while rebuilding unused pane list in a preferential order
    work, unused = unused, ""
    lastpaneid = ""
    for paneid in list(newpanes):
        if paneid in PANE_CHARACTERS: lastpaneid = paneid # Last valid paneid
        if paneid in work and paneid not in used: unused += paneid # Ignore invalid panes
    work, used = PaneList_MovePanes( work, used, unused )
    # Combine by next highest match
    ix = 0 # In case of empty set
    for chkix, paneid in enumerate(list(work)):
        if PANE_CHARACTERS.find(paneid) >= PANE_CHARACTERS.find(lastpaneid): ix = chkix ; break
    unused += work[ix:] + work[:ix] # Ordered by assignment availability, rooted by lastpaneid
    # Return both (note only unused is preferentially reordered)
    return used, unused

##
## Flex: Other macros
##

def panes_in_use_message_generate(panes_in_use):
    if not panes_in_use:
        return None
    print_panes = "pane" + ("s" if len(panes_in_use) > 1 else "")
    print_isare = "are" if len(panes_in_use) > 1 else "is"
    return "Specified " + print_panes + " (" + panes_in_use + ") " + print_isare + " already in use"

##
## Decorator for building flex commands
##

class flex(object):
    def __init__(self, command="", examples=[], description=None, aliases=[], group=""):
        self.command_only = command
        self.description = description
        self.examples = examples
        self.aliases = aliases
        self.group = group
    def __call__(self, function):
        # From function build usage
        self.usage = self.command_only
        self.arglens = [ 0, 0 ] # [ Required, Total ]
        spec = inspect.getargspec(function)
        la = len(spec.args) if spec.args else 0
        ld = len(spec.defaults) if spec.defaults else 0
        class NoDefault: pass # Placeholder since None is a valid default argument
        args_with_defaults = [ ( spec.args[ix], (NoDefault if ix < la-ld else spec.defaults[ix-(la-ld)]) ) \
            for ix in range(0, len(spec.args)) ]
        brackets = lambda optional: "[]" if optional else "<>"
        def tagged(arg, tag): return True if tag in arg else False
        def clipped(arg, tags):
            arg = arg
            for tag in tags:
                if arg.find(tag) >= 0: arg = arg[:arg.find(tag)] + arg[arg.find(tag)+len(tag):]
            return arg
        for arg, default in args_with_defaults:
            # Regular argument types (normally required):
            #       _PRIVATE    This argument is never shown to the user
            #       _OPTIONAL   Listed as optional even if a default parameter was not specified
            #       =Default    Listed as optional if a default parameter was specified
            if not tagged(arg, "_PRIVATE"):
                self.arglens[1] += 1
                if default is NoDefault: self.arglens[0] += 1
                optional = True if tagged(arg, "_OPTIONAL") else False
                arg = clipped( arg, ["_OPTIONAL"] ) # Clip markers before printing
                enclosed = brackets( default is not NoDefault or optional )
                self.usage += " " + enclosed[0] + arg + enclosed[1]
        if spec.varargs:
            # Variable argument types (normally optional):
            #       _REQUIRED   Makes the parameter required where it is normally optional
            varargs = spec.varargs
            required = optional = False
            required = True if tagged(varargs, "_REQUIRED") else False
            varargs = clipped( varargs, ["_REQUIRED"] ) # Clip markers before printing
            enclosed = brackets( not required )
            self.usage += " " + enclosed[0] + varargs + "..." + enclosed[1]
            if required: self.arglens[0] += 1 # If required then varargs is [REQ+1, -1] instead of [REQ, -1]
            self.arglens[1] = -1 # Represents use of *args
        # Adds new menu item, or appends usage and examples if it already exists
        # Description is only used on first occurrence of the command, successive commands append without description
        append = False
        for entdict in flexmenu:
            if entdict['about'][0] == self.command_only:
                entdict['funcs'] += [ function ]
                entdict['usage'] += [ self.usage, self.examples, self.arglens ]
                entdict['group'] += [ self.group ]
                append = True
        if not append:
            flexmenu.append( {
                'funcs': [ function ],
                'about': [ self.command_only, self.description ],
                'usage': [ self.usage, self.examples, self.arglens ],
                'group': [ self.group ]
            } )
            if not self.command_only in flexmenu_list: flexmenu_list.append( self.command_only )
        # Add aliases if any
        for ix, alias_tup in enumerate(self.aliases):
            if type(alias_tup) is not list:
                print("Flex command indexing error: " + self.command_only + " alias #" + str(1+ix) + " is not a list")
                exit()
            if len(alias_tup) != 2:
                print("Flex command indexing error: " + self.command_only + " alias #" + str(1+ix) + " is not a pair")
                exit()
            flexmenu_aliases.append( alias_tup )
        # Grouped commands
        if not self.group in flexmenu_grouped: flexmenu_grouped[self.group] = []
        if not self.command_only in flexmenu_grouped[self.group]:
            flexmenu_grouped[self.group].append(self.command_only)
        # Function wrapper
        def wrapper(*args):
            return function(*args)
        return wrapper

##
## Table Printer (used by help and list)
##

def table(output, markers, marklines, title, contents):
    def table_divider(marker, row):
        output.append(marker + "+-" + "-+-".join( [ len(col) * "-" for col in row ] ) + "-+")
    def table_line(marker, row):
        output.append(marker + "| " + " | ".join( [ col for col in row ] ) + " |")
    # Count columns
    columns = 0
    for row in contents:
        if len(row) > columns: columns = len(row)
    # Maximum width of each column, taking into account title and all lines
    widths = [ len(col) for col in title ]
    for line in contents: widths = [ l if l > n else n for l, n in zip( widths, [ len(n) for n in line ] ) ]
    # Pad all lines
    contents.insert( 0, title )
    contents_unpadded = contents
    contents = []
    for line in contents_unpadded:
        contents.append( [ l + ((((w - len(l)) if len(l) < w else 0)) * " ") for w, l in zip( widths, line ) ] )
    if columns:
        first = True
        line = 0
        for row in contents:
            line += 1
            marker = markers[1] if line in marklines else markers[0]
            if first: table_divider( markers[0], row )
            table_line( marker, row )
            if first: table_divider( markers[0], row )
            first = False
        table_divider( markers[0], row )
        output.append("")

##
## Commands: Helpers
##

@flex(
    command     = "help",
    group       = "helpers",
    description = "Show information for one or more commands",
)
def cmd_help_0():
    return cmd_help_N() # Wrapper

@flex(
    command     = "help",
    group       = "helpers",
    examples    = [ "help new scale" ],
    aliases     = [ ["?", "help "], ["/", "help "] ],
)
def cmd_help_N(*commands):
    # Filter specified commands into a list of unique commands, sorted by the official command order
    args = commands
    commands = []
    for arg in args:
        if arg not in commands:
            commands.append(arg)
    commands = [ cmd_dict['about'][0] for cmd_dict in flexmenu if cmd_dict['about'][0] in commands ]
    # Macros
    lengths = lambda name, about, usage, example: [ len(name), len(about), len(usage), len(example) ]
    # All menus are four columns representing: name, about, usage, example
    menu_title = [ "Command", "Description", "Usage", "Examples" ]
    menu_lines = [] # Printed columns, not padded
    # Build menu print list from all known commands
    add = lambda name="", about="", usage="", example="": menu_lines.append( [ name, about, usage, example ] )
    for cmd_dict in flexmenu:
        if commands and cmd_dict['about'][0] not in commands: continue
        fnew = True
        name, about = cmd_dict['about']
        for usage, examples, arglens in usage_triplets(cmd_dict):
            fuse = True
            if not examples: examples = [ None ] # Allow usage without a corresponding example
            for example in examples: # Add to menu_lines
                if fnew: add()
                add( name if fnew else "", about if fnew else "", usage if fuse else "", example if example else "" )
                fnew = fuse = False
        if fnew:
            add()
            add( name, about )
    add()
    # Spread the description over multiple lines, adding blank lines where necessary
    # Note: Only the about column ("Description") supports word-wrap
    lines = menu_lines
    menu_lines = []
    width = 60
    carry = ""
    for name, about, usage, example in lines:
        def recursive_carry(carry, name, about, usage, example): # carry
            def carry_on(about, carry): # about, carry
                if len(about) > width:
                    hardbreak = width # In the event the max width exceeds a word width
                    for ix in range(width-1, -1, -1):
                        if about[ix] == " " or about[ix] == "\t":
                            hardbreak = ix
                            break
                    if about[hardbreak] == " " or about[hardbreak] == "\t":
                        carry, about = about[hardbreak+1:].strip(), about[:hardbreak].strip()
                else:
                    carry = ""
                return about, carry
            if carry:
                about = carry
                about, carry = carry_on( about, carry )
                add( name, about, usage, example )
                about = ""
                if not name+about+usage+example:
                    # Inserting new lines to list to accommodate a lengthy description
                    return recursive_carry( carry, name, about, usage, example )
                return carry
            about, carry = carry_on( about, carry )
            add( name, about, usage, example )
            return carry
        carry = recursive_carry( carry, name, about, usage, example )
    # Print introduction
    flexsense['output'].append( "  Flex menu" + ((" (" + ", ".join(commands) + ")") if len(commands) else "") + ":" )
    flexsense['output'].append( "" )
    # Print menu table
    table( flexsense['output'], ["    ", "    "], [], menu_title, menu_lines )

##
## Commands: Selectors
##

@flex(
    command     = "list",
    group       = "selectors",
    description = "List all available windows in this tmuxomatic session",
)
def cmd_list():
    flexsense['output'].append( "  Available windows in this session file (use serial number or name):" )
    flexsense['output'].append( "" )
    list_lines = [] # Printed columns, not padded
    for serial in range(1, flexmenu_session.Count_Windows()+1):
        number_str = str(serial)
        name = flexmenu_session.Get_Name(serial)
        dimensions_int = flexmenu_session.Get_WindowgramDimensions_Int(serial) # Use this to avoid reinitialization
        dimensions_str = str(dimensions_int[0]) + "x" + str(dimensions_int[1])
        wg = flexmenu_session.Get_Wg( serial )
        used, unused = wg.Panes_GetUsedUnused()
        panecount = str(len(used))
        list_lines.append( [ number_str, dimensions_str, panecount, name ] )
    if not list_lines:
        flexsense['output'].append( "    There are no windows, create one with: new <name>" )
        flexsense['output'].append( "" )
    else:
        selected = []
        if flexmenu_index[0]: selected.append( flexmenu_index[0] + 1 ) # Skip title line
        list_title = [ "Window", "Dimensions", "Panes", "Name" ]
        table( flexsense['output'], ["    ", " -> "], selected, list_title, list_lines )

@flex(
    command     = "use",
    group       = "selectors",
    examples    = [ "use my example", "use 1" ],
    description = "Select the window you would like to modify",
)
def cmd_use(*name_or_serial_REQUIRED):
    name_or_serial = " ".join(name_or_serial_REQUIRED)
    def using(serial):
        flexmenu_index[0] = serial
        wg = flexmenu_session.Get_Wg(serial)
        if wg.Analyze_IsBlank():
            flexmenu_session.Replace_Windowgram(serial, "1")
            wg = flexmenu_session.Get_Wg(serial)
            return flexsense['notices'].append( FlexWarning( "The windowgram was blank and required initialization" ) )
    if name_or_serial.isdigit():
        serial = int(name_or_serial)
        if flexmenu_session.Serial_Is_Valid(serial): return using(serial)               # Serial match
    for serial in range(1, flexmenu_session.Count_Windows()+1):
        if name_or_serial == flexmenu_session.Get_Name(serial): return using(serial)    # Exact string match
    matches = matched = 0
    for serial in range(1, flexmenu_session.Count_Windows()+1):
        if flexmenu_session.Get_Name(serial).startswith(name_or_serial):
            matched = serial ; matches += 1
    if matches == 1: return using(matched)                                              # Starting string match
    if matches:
        return flexsense['notices'].append( FlexError( "The name \"" + \
            name_or_serial + "\" is ambiguous (" + str(matches) + " matches)" ) )       # Name ambiguous
    else:
        return flexsense['notices'].append( FlexError( \
            "This name or serial is invalid: " + name_or_serial ) )                     # No match
    flexsense['output'].append( "" )

@flex(
    command     = "new",
    group       = "selectors",
    examples    = [ "new some feeds" ],
    description = "Create a new window, initialized to '1'",
)
def cmd_new(*window_name_REQUIRED):
    name = " ".join(window_name_REQUIRED)
    for serial in range(1, flexmenu_session.Count_Windows()+1):
        if name == flexmenu_session.Get_Name(serial):
            return flexsense['notices'].append( FlexError( \
                "The name \"" + name + "\" is already in use, try another" ) )
    # Create window
    comments = "## Window added by tmuxomatic flex " + VERSION + "\n\n"
    serial = flexmenu_session.Add_Windowgram( comments, name, "1" )
    # Use it
    cmd_use(*[str(serial)])

##
## Commands: Printers ... Mainly a pseudo-group to keep print out of the quick menus
##

@flex(
    command     = "print",
    group       = "printers",
    description = "Display windowgram (automatic if there is no other output)",
    aliases     = [ [".", "print "], ],
)
def cmd_print():
    serial = flexmenu_index[0]
    if flexmenu_session.Serial_Is_Valid(serial):
        flexsense['output'].append( "\n".join([ "    " + l \
            for l in flexmenu_session.Get_Windowgram(serial).split("\n") ]) )

##
## Commands: Modifiers
##

@flex(
    command     = "scale",
    group       = "modifiers",
    examples    = [ "scale 25", "scale 500%", "scale 2x", "scale 64:36" ],
    description = "Scale the windowgram.  Valid parameters are multipliers (x), percentages (%), exact character " + \
                  "dimensions, or any combination thereof.  Use a space ( ), colon (:), or times (x) to separate " + \
                  "the x and y axis.  If only one axis is specified then the value will be applied to both x and y.",
    aliases     = [ ["resize", "scale "],
                    ["half", "scale 50%"], ["double", "scale 2x"],
                    ["wider", "scale 200%:100%"], ["thinner", "scale 50%:100%"],
                    ["taller", "scale 100%:200%"], ["shorter", "scale 100%:50%"],
                    ["higher", "scale 100%:200%"], ["lower", "scale 100%:50%"], ],
)
def cmd_scale_1(wg_PRIVATE, xy_how): # 1 parameter
    # Split directives like "64:36" and "64x36" into "64 36", also works using percentages "200%:50%", or using
    # multipliers "2x:2x" as long as ":" is used instead of "x" as there would be a conflict with the multiplier
    # TODO: This could be more flexible to cover cases like "2xx2" and "2x2x" by using regex
    xy_spl = None
    if xy_how.count("x") == 1 and xy_how[-1:] != "x": xy_spl = xy_how.split("x")
    elif xy_how.count(":") == 1: xy_spl = xy_how.split(":")
    if xy_spl and len(xy_spl) == 2: return cmd_scale_2( wg_PRIVATE, *xy_spl )
    # Others are simply cloned like "2x" into "2x 2x"
    return cmd_scale_2( wg_PRIVATE, xy_how, xy_how )

@flex(
    command     = "scale",
    group       = "modifiers",
    examples    = [ "scale 25 15", "scale 200% 50%", "scale 2x .5x" ],
)
def cmd_scale_2(wg_PRIVATE, x_how, y_how): # 2 parameters
    # Because text is inherently low resolution, fractional scaling may produce unsatisfactory results
    if not wg_PRIVATE:
        return flexsense['notices'].append( FlexError( "Please specify a window with use or new" ) )
    # Generics
    wg_before = wg_PRIVATE
    dim_before = wg_before.Analyze_WidthHeight()
    # Convert to common float multipliers for easy scaling
    args = [ dim_before[0], dim_before[1] ] # Default to no scale on error
    for ix, arg in enumerate([x_how, y_how]):
        args[ix] = size_ConvertToCharacters(arg, dim_before[ix])
        if args[ix] is None:
            return flexsense['notices'].append( FlexError( "Invalid size parameter: " + arg ) )
    w_chars, h_chars = args
    # Scale the windowgram
    wg_after = Windowgram( scalecore( wg_before.Export_String(), w_chars, h_chars ) )
    # Verify new windowgram (in case of scale error)
    dim_result = wg_after.Analyze_WidthHeight()
    if not dim_result[0] or not dim_result[1]:
        return flexsense['notices'].append( FlexError( "Scale produced a blank windowgram, skipping" ) )
    if dim_result[0] != w_chars or dim_result[1] != h_chars:
        return flexsense['notices'].append( FlexError( "Scale produced erroneous result, skipping" ) )
    # Alert user to any panes lost
    lost_panes = PaneList_DiffLost( wg_before, wg_after )
    if len(lost_panes):
        flexsense['notices'].append( FlexWarning( "Lost " + str( len(lost_panes) ) + " panes: " + lost_panes ) )
    # Replace windowgram
    wg_PRIVATE.Import_Wg( wg_after )

@flex(
    command     = "add",
    group       = "modifiers",
    examples    = [ "add right 50% A", "add b 3", "add l .5x" ],
    description = "Append pane to windowgram edge.  Edge is identified by name (e.g., right), or a variety of " + \
                  "abbreviations (e.g., r, rt).  The size of the pane may be defined as an exact character size, " + \
                  "a percentage (%), or a multiplier (x).  If a pane id is not specified, lowest available will " + \
                  "be used.",
    aliases     = [ ["append", "add "], ["app", "add "] ],
)
def cmd_add(wg_PRIVATE, edge, size, newpane=None):
    # TODO: Edge could also represent a combined edge of panes.  The panes would have to be adjacent, but it would
    # allow for the insertion of panes into the middle of windows.  Would require a bit of recursive acrobatics to
    # scale the surrounding panes to support the insertion, but it could be done.  This is the insert command, and
    # the accommodation logic is the same as clone.
    if not wg_PRIVATE:
        return flexsense['notices'].append( FlexError( "Please specify a window with use or new" ) )
    wg = wg_PRIVATE
    newpane, error = wg.Panes_GetNewPaneId( newpane )
    if error:
        return flexsense['notices'].append( FlexError( "Unable to secure a new pane id: " + error ) )
    # Convert axis-flag to ix to avoid rewrite
    axis_as_vh, negate_flag = direction_to_axiswithflag(edge)
    if axis_as_vh == "v" and negate_flag == False: ix = 0   # Top
    elif axis_as_vh == "v" and negate_flag == True: ix = 1  # Bottom
    elif axis_as_vh == "h" and negate_flag == True: ix = 2  # Right
    elif axis_as_vh == "h" and negate_flag == False: ix = 3 # Left
    else: ix = None
    # Process
    if ix is not None:
        # ix = 0123 == TBRL | NSEW
        windowgram_lines = wg.Export_Lines()
        axis_length = len(windowgram_lines) if (ix == 0 or ix == 1) else len(windowgram_lines[0])
        axis_width = len(windowgram_lines) if (ix == 2 or ix == 3) else len(windowgram_lines[0])
        size_chars = size_ConvertToCharacters( size, axis_length )
        if size_chars is None:
            return flexsense['notices'].append( FlexError( "Invalid size parameter: " + size ) )
        if ix == 0: # Top
            for _ in range( size_chars ): windowgram_lines.insert( 0, newpane * axis_width )
        elif ix == 1: # Bottom
            for _ in range( size_chars ): windowgram_lines.append( newpane * axis_width )
        elif ix == 2: # Right
            windowgram_lines = [ line + (newpane * size_chars) for line in windowgram_lines ]
        elif ix == 3: # Left
            windowgram_lines = [ (newpane * size_chars) + line for line in windowgram_lines ]
        # Detect when addition doesn't register and notify user as warning
        wg_compare_before = wg.Export_String()
        wg.Import_Lines( windowgram_lines )
        wg_compare_after = wg.Export_String()
        if wg_compare_before == wg_compare_after:
            return flexsense['notices'].append( FlexWarning( "Addition was too small to register" ) )
        # Replace windowgram
        wg_PRIVATE.Import_Wg( wg )
        # Done
        return
    # Edge not found
    return flexsense['notices'].append( FlexError(
        "The edge you specified is invalid, please specify either: top, bottom, left, or right" ) )

@flex(
    command     = "break",
    group       = "modifiers",
    examples    = [ "break 1 3x3", "break 0 3x1 x", "break z 3x2 IVXLCD" ],
    description = "Break a pane into a grid of specified dimensions.  If the break does not produce even panes at " + \
                  "the specified resolution, it will automatically scale up to the next best fit.  The newpanes " + \
                  "parameter is an optional starting pane id, or pane rename sequence.",
    aliases     = [ ["grid", "break "], ["panes", "break "], ],
)
def cmd_break(wg_PRIVATE, pane, grid, newpanes=None):
    # Analogues:
    #       Break may be used for split 50%
    # Notes:
    #       An example of avoiding unnecessary complexity: It's easy to incorporate support for group as target.  Such
    #       an algorithm would break all panes in group equally and apply newpanes linearly.  But things become complex
    #       quickly if it were to avoid size explosions by finding the most efficient break sequence (common divisors).
    #       Besides, such situations are easily managed by the user of flex; simply break them one by one in a sequence
    #       that yields personally satisfactory results.  Because this is already possible with flex, such a feature
    #       would only add complexity without achieving a practical function.
    if not wg_PRIVATE:
        return flexsense['notices'].append( FlexError( "Please specify a window with use or new" ) )
    # In order to produce a break of even proportions, we have to scale this windowgram up to next best fit.  It
    # could go one step further and find the most optimal size, being a resolution that evenly scales the original
    # windowgram constituent panes, while simultaneously providing a grid of even sizes.  The problem is that common
    # use cases would result in massive sizes to accommodate; though accurate, it would not be very practical.
    wg = wg_PRIVATE
    used, unused = wg.Panes_GetUsedUnused()
    if pane not in PANE_CHARACTERS:
        return flexsense['notices'].append( FlexError( "The pane you specified is invalid" ) )
    elif pane in unused:
        return flexsense['notices'].append( FlexError( "The pane you specified does not exist" ) )
    # Grid analysis and validity check
    gw = gh = panes = 0
    reason = "Grid parameter is invalid: " + grid
    if grid.count("x") == 1:
        gw, gh = grid.split("x")
        if gw.isdigit() and gh.isdigit():
            gw, gh = int(gw), int(gh)
            panes = gw * gh
            len_unused = len(unused) + 1 # The +1 accounts for the target pane that becomes available
            if not panes:
                reason = "Grid you specified results in no panes"
            elif panes > len(PANE_CHARACTERS):
                reason = "Grid is " + str(panes) + " panes, exceeding max of " + str(len(PANE_CHARACTERS))
            elif panes > len_unused:
                reason = "Grid is " + str(panes) + " panes, only " + str(len_unused) + " will be available"
            else:
                reason = None # No error
    if reason is not None:
        return flexsense['notices'].append( FlexError( reason ) )
    # Extract the dimensions of the pane to determine requisite scale (if any)
    wg_w, wg_h = wg.Analyze_WidthHeight()
    px, py, pw, ph = wg.Panes_PaneXYWH( pane )
    # Perform a scale if needed
    scale_to = lambda r1, r2: (((float(int(r1/r2))+1.0)*r2) if (r1 % r2) else r1) if (r1 > r2) else r2
    scale_to_pane_w = int( scale_to( float(pw), float(gw) ) ) # Pane target x
    scale_to_pane_h = int( scale_to( float(ph), float(gh) ) ) # Pane target y
    stw_w = int(float(wg_w) * float(scale_to_pane_w) / float(pw)) # Window target x
    stw_h = int(float(wg_h) * float(scale_to_pane_h) / float(ph)) # Window target y
    # Scale
    wg_new = Windowgram( scalecore(
        wg.Export_String(), stw_w, stw_h, ( pane, scale_to_pane_w, scale_to_pane_h ) ) )
    _, _, npw, nph = wg_new.Panes_PaneXYWH( pane )
    # Validate
    if (npw != scale_to_pane_w or nph != scale_to_pane_h):
        return flexsense['notices'].append( FlexError( "The result is not the expected pane size" ) )
    # Swap
    wg = wg_new
    # Dimensions must be reloaded in the event that the windowgram was scaled
    wg_w, wg_h = wg.Analyze_WidthHeight()
    px, py, pw, ph = wg.Panes_PaneXYWH( pane )
    # Manually move availability of pane so it may be reused
    used, unused = PaneList_MovePanes( used, unused, pane )
    # Set starting panes.  By default this starts at the lowest unused pane id and iterates forward.  However
    # the user may specify a pane to start the iteration at, for example if it's a 3x2 grid (6 panes produced):
    #   specified == (None)    produces == 012345
    #                A                     ABCDEF
    #                BLN                   BLNOPQ
    #                BLN1                  BLN123
    if newpanes:
        panes_in_use = "".join([ch for ch in newpanes if ch not in unused and ch != pane])
        panes_in_use_message = panes_in_use_message_generate( panes_in_use )
        if panes_in_use_message:
            return flexsense['notices'].append( FlexError( panes_in_use_message ) )
        used, unused = newpanes_RebuildPaneListsInPreferentialOrder( used, unused, newpanes )
    # Replace pane with grid
    windowgram_lines = wg.Export_Lines()
    wg.Import_Lines( [
        "".join( [ ch if ch != pane else unused[int((iy-py+1)*gh/ph)*gw+int((ix-px+1)*gw/pw)] \
            for ix, ch in enumerate(list(line)) ] ) for iy, line in enumerate(windowgram_lines)
    ] )
    # Replace windowgram
    wg_PRIVATE.Import_Wg( wg )

@flex(
    command     = "join",
    group       = "modifiers",
    examples    = [ "join abcd efgh", "join abcd.x efgh.y" ],
    description = "Join a contiguous group of panes into a single pane.  Multiple joins are supported.  The joined " + \
                  "pane is named after the first pane specified, but can be renamed by adding dot (.) followed by " + \
                  "the pane id.",
    aliases     = [ ["group", "join "], ["merge", "join "], ["glue", "join "], ],
)
def cmd_join(wg_PRIVATE, *groups_REQUIRED):
    # Analogues:
    #       Join may be used for rename: join <old>.<new>
    #       Join may be used for swap: join <one>.<two> <two>.<one>
    # Notes:
    #       Join could be seen as a type of rename, and was used for rename and swap prior to those implementations
    groups = groups_REQUIRED # Readability
    argument = lambda ix: str(ix+1) + " (\"" + groups_REQUIRED[ix] + "\")" # Show the group that the user specified
    if not wg_PRIVATE:
        return flexsense['notices'].append( FlexError( "Please specify a window with use or new" ) )
    wg = wg_PRIVATE
    # Repackage groups so all have the rename element
    work, groups = groups, []
    for group in work: groups.append( group if "." in group else (group + "." + group[0]) )
    # Walk all groups and build join lists
    panes_clipped = ""
    for ix, group in enumerate(groups):
        try:
            # Make sure group is superficially valid
            if group.count(".") > 1: raise Exception("Argument contains more than one rename delimiter")
            invalids = "".join([ ch for ch in set(group) if ch not in PANE_CHARACTERS and ch != "." ])
            if invalids: raise Exception("Group contains invalid characters: " + invalids)
            # Verify rename and quietly strip duplicate panes
            group_l, group_r = group.split(".")
            if len(group_r) == 0: raise Exception("Rename delimiter used but subsequent pane unspecified")
            if len(group_r) > 1: raise Exception("Only one pane should be specified after the rename delimiter")
            group = "".join( [ ch for ch in sorted(set(group_l), key=lambda x: group.find(x)) ] ) + "." + group_r
            # Build group, simulate clip, test presence
            notfound = ""
            for ch in [ ch for ch in PANE_CHARACTERS if ch in set(group.split(".")[0]) ]: # Ordered set
                if ch in panes_clipped: raise Exception("Pane \"" + ch + "\" was already used by a previous group")
                if not wg.Panes_HasPane( ch ): notfound += ch
                else: panes_clipped += ch
            if notfound:
                raise Exception("Windowgram does not have pane" + ("(s) " if len(notfound)-1 else " ") + notfound)
        except Exception as error:
            return flexsense['notices'].append( FlexError(
                "Error with argument " + argument(ix) + ": " + str(error) ) )
    # Test the duplication of target panes by matching them against availability adjusted for panes clipped
    used, unused = wg.Panes_GetUsedUnused()
    used = "".join(list(set(used) - set(panes_clipped)))
    unused = "".join( [ ch for ch in PANE_CHARACTERS if ch in (unused + panes_clipped) ] )
    for ix, group in enumerate(groups):
        try:
            group_l, group_r = group.split(".")
            if group_r in used:
                raise Exception("Attempting to rename to pane " + group_r + " when it's in use")
            used += group_r
        except Exception as error:
            return flexsense['notices'].append( FlexError(
                "Error with argument " + argument(ix) + ": " + str(error) ) )
    # Perform the joins, detecting pane gaps in the group, resulting windowgram is paired for later merging
    joins = []
    for group in groups:
        # Join preprocessing
        group_l, group_r = group.split(".")
        result, suggestions = groupcore(wg, group_l)
        if result is GroupStatus.Invalid_Panes: # Occurs if groupcore() panes parameter is invalid
            return flexsense['notices'].append( FlexError(
                "Group #" + argument(ix) + " contains invalid panes" ) )
        if result is GroupStatus.Insufficient_Panes:
            return flexsense['notices'].append( FlexError(
                "Group #" + argument(ix) + " isn't whole, but it would be if you add: " + suggestions ) )
        # Join ... By now the group is fully vetted: entirely valid, rectangularly whole
        pair_w = Windowgram( wg.Export_String() )
        pair_m = Windowgram_Mask_Generate( pair_w, group_l )
        pair_w.Panes_Renamer( group_l, group_r )
        joins.append( [ pair_w, pair_m ] )
    # A separate merge step is required to prevent name conflicts where the user makes use of the rename option.
    wg.Import_Mosaic( ( wg, joins ) )
    # Replace windowgram
    wg_PRIVATE.Import_Wg( wg )

@flex(
    command     = "split",
    group       = "modifiers",
    examples    = [ "split 1 bottom 3", "split 1 vertical -3", "split 0 left 25% LR" ],
    description = "Splits one pane on either: an axis (vert, horz), or from an edge (top, left).  For an axis, a " + \
                  "negation of size inverses the split.  Size parameter is optional, the default is 50%.  Optional " + \
                  "newpanes parameter will rename the panes in order of newest to oldest (2 panes maximum).",
)
def cmd_split(wg_PRIVATE, pane, how, size=None, newpanes=None):
    # Analogues:
    #       Break may be used for split 50%
    # Expectations (for testing):
    #       If any of the specified newpanes are invalid, return error
    #       A negative flag for edges (tblr) is ignored, but used for axis (vh)
    # TODO:
    #       Possible reordering detection, "split v h" (where "v" is the pane)
    #           Senses reordering, e.g. "split horz v", and if unable to determine defaults to pane first
    if not wg_PRIVATE:
        return flexsense['notices'].append( FlexError( "Please specify a window with use or new" ) )
    wg = wg_PRIVATE
    used, unused = wg.Panes_GetUsedUnused()
    axis = how # This argument is handled as an axis
    # Set the default size if unspecified
    if size is None: size = "50%"
    # Verify pane
    if pane not in PANE_CHARACTERS:
        return flexsense['notices'].append( FlexError( "The pane you specified is invalid" ) )
    elif pane in unused:
        return flexsense['notices'].append( FlexError( "The pane you specified does not exist" ) )
    # Verify axis and reduce to "v" or "h"
    inverse = "-" if size[0] == "-" else ""
    if is_axis_vert(axis): axis = "v"
    elif is_axis_horz(axis): axis = "h"
    else:
        if size[0] == "-":
            return flexsense['notices'].append( FlexError( "Negative size only valid if `how` is vert or horz" ) )
        axis, negate_flag = direction_to_axiswithflag(axis)
        if axis is None or negate_flag is None:
            return flexsense['notices'].append( FlexError( "The axis you specified is invalid" ) )
        inverse = "-" if negate_flag else ""
    # Get axis_length
    px, py, pw, ph = wg.Panes_PaneXYWH(pane)
    axis_length = pw if axis == "h" else ph
    # Verify pane is large enough to split
    if pw < 2 and ph < 2: # Single character pane
        return flexsense['notices'].append( FlexError( "Pane is too small to be split" ) )
    if axis_length < 2: # Single character length on the specified axis
        return flexsense['notices'].append( FlexError( "Pane is too small to be split in that way" ) )
    # Verify size
    original_size = size # Retain original for error messages
    while size and size[0] == "-": size = size[1:] # Strip negation
    size_type = size_GetType( size )
    if size_type is None:
        return flexsense['notices'].append( FlexError( "Invalid size parameter: " + original_size ) )
    if size_GreaterOrEqualToBaseCharacters( size, axis_length ):
        rep = inverse
        if size_type == "characters": rep += str(axis_length)
        elif size_type == "percentage": rep += "100%"
        elif size_type == "multiplier": rep += "1x"
        return flexsense['notices'].append( FlexError( "Specified size (" + original_size + \
            ") is greater or equal to the maximum range (" + rep + ") of this function" ) )
    size_chars = size_ConvertToCharacters( size, axis_length )
    if size_chars is None:
        return flexsense['notices'].append( FlexError( "Invalid size parameter: " + size ) )
    if size_chars >= axis_length: # Shouldn't happen by now, but if it does
        return flexsense['notices'].append( FlexError( "Resulting size (" + inverse + str(size_chars) + \
            " characters) is greater or equal to the axis length (" + str(axis_length) + ")" ) )
    if inverse: size_chars = axis_length - size_chars # Flip
    # Verify newpanes ... Set to first available if not specified
    if len(unused) < 1: return flexsense['notices'].append( FlexError( "Insufficient panes available for a split" ) )
    if newpanes is None: newpanes = ""
    if len(newpanes) == 0: newpanes += unused[0] # New pane is first available
    if len(newpanes) == 1: newpanes += pane # Base pane
    if len(newpanes) > 2: return flexsense['notices'].append( FlexError(
        "Parameter newpanes exceeds the function maximum of two panes" ) )
    for ch in set(newpanes):
        if not ch in PANE_CHARACTERS: return flexsense['notices'].append( FlexError(
            "Invalid pane in newpanes parameter: " + ch ) )
    panes_in_use = "".join([ch for ch in newpanes if ch not in unused and ch != pane])
    panes_in_use_message = panes_in_use_message_generate( panes_in_use )
    if panes_in_use_message: return flexsense['notices'].append( FlexError( panes_in_use_message ) )
    used, unused = newpanes_RebuildPaneListsInPreferentialOrder( used, unused, newpanes )
    # Reorder the newpanes to match fill logic expectations
    newpanes = newpanes[:2] if not inverse else newpanes[1::-1]
    # Perform the split
    src_lines, dst_lines = wg.Export_Lines(), []
    sx, sy = px + size_chars if axis == "h" else 0, py + size_chars if axis == "v" else 0
    for iy, line in enumerate(src_lines):
        if axis == "v": line = "".join( [ newpanes[0 if iy < sy-1 else 1] if ch == pane else ch \
            for ch in list(line) ] )
        if axis == "h": line = "".join( [ newpanes[0 if ix < sx-1 else 1] if ch == pane else ch \
            for ix, ch in enumerate(list(line)) ] )
        dst_lines.append( line )
    wg.Import_Lines( dst_lines )
    # Replace windowgram
    wg_PRIVATE.Import_Wg( wg )

@flex(
    command     = "rename",
    group       = "modifiers",
    examples    = [ "rename Ff Tt", "rename F T f t" ],
    description = "Rename from one pane or group, to another pane or group, paired as <from> <to>.  Multiple " + \
                  "pairs may be specified.",
)
def cmd_rename(wg_PRIVATE, panes_from, *panes_to):
    # Analogues:
    #       Join may be used for rename: join <old>.<new>
    #       Rename may be used for swap: rename <old><new> <new><old>
    # Tests:
    #       new rename.t1 ; break 1 3x2 ABCabc ; rename AaBb BbAa
    #       new rename.t2 ; break 1 3x2 ABCabc ; rename Aa Bb Bb Cc Cc Aa
    #       new rename.t3 ; break 1 2x2 1 ; rename 12 21 34 43
    #       new rename.t4 ; break 1 2x2 1 ; rename 1 2 2 1 3 4 4 3
    if not wg_PRIVATE:
        return flexsense['notices'].append( FlexError( "Please specify a window with use or new" ) )
    # This command could have wrapped join, but a native implementation has been made to reduce overhead somewhat
    wg = wg_PRIVATE
    used, unused = wg.Panes_GetUsedUnused()
    pairs = [ panes_from ] + [ arg for arg in panes_to ]
    if len(pairs)&1:
        return flexsense['notices'].append( FlexError( "Insufficient data, every <from> must be followed by <to>" ) )
    pairs = [ pairs[i*2:i*2+2] for i in range(len(pairs)>>1) ]
    # Ends parsed separately to allow for any pair ordering, this parallel effect is also supported by the join command
    def proc_list(which): # error or None
        nonlocal save_f, work_f, work_t
        pair = "1"
        for f, t in pairs:
            # Counts must match (1:1)
            if len(f) != len(t):
                return "Pair " + pair + " count error, both <from> and <to> pane counts must be identical"
            # Check for self rename (this could be safely ignored)
            selfrename = [ fi for fi, ti in zip(list(f), list(t)) if fi == ti ]
            if selfrename:
                return "Pane `" + selfrename[0] + "` renames to self in pair " + pair
            # Iterate all panes in this argument and validate
            fort = f if not which else t
            for paneid in fort:
                if not paneid in PANE_CHARACTERS:
                    return "Invalid pane `" + paneid + "` in pair " + pair
                if which == 0: # Only From
                    if paneid in work_f: # The pane must not have been previously freed
                        return "The <from> pane `" + paneid + "` in pair " + pair + " was renamed by another pair"
                    if not paneid in used: # The pane must already be in use
                        return "The <from> pane `" + paneid + "` in pair " + pair + " is not being used"
                if which == 1: # Only To
                    if paneid in work_t: # The pane must not have been previously named
                        return "The <to> pane `" + paneid + "` in pair " + pair + " was already named by another pair"
                    if not paneid in unused + save_f: # The pane must be unavailable
                        return "The <to> pane `" + paneid + "` in pair " + pair + " is already being used"
            # Next
            work_f += f
            work_t += t
            pair = str( int(pair) + 1 )
        return None
    # Validate pair lists in order of: from, to
    work_f = work_t = save_f = ""
    error = proc_list(0) # From
    if error: return flexsense['notices'].append( FlexError( error ) )
    save_f, work_f, work_t = work_f, "", "" # Retention required for second pass validation
    error = proc_list(1) # To
    if error: return flexsense['notices'].append( FlexError( error ) )
    # Perform the renames independently, result is paired with a mask and stored in a list for use in a mosaic
    renames = []
    for f, t in pairs:
        for pf, pt in zip(f, t):
            # Rename ... By now fully vetted
            pair_w = Windowgram( wg.Export_String() )
            pair_m = Windowgram_Mask_Generate( pair_w, pf )
            pair_w.Panes_Renamer( pf, pt )
            renames.append( [ pair_w, pair_m ] )
    # A separate merge step is required
    wg.Import_Mosaic( ( wg, renames ) )
    # Replace windowgram
    wg_PRIVATE.Import_Wg( wg )

@flex(
    command     = "swap",
    group       = "modifiers",
    examples    = [ "swap A B", "swap Aa Bb 1 2" ],
    description = "Swaps one pane or group, with another pane or group, paired as <from> <to>.  Multiple " + \
                  "pairs may be specified.",
)
def cmd_swap(wg_PRIVATE, panes_from, *panes_to):
    # Analogues:
    #       Join may be used for swap: join <one>.<two> <two>.<one>
    #       Rename may be used for swap: rename <old><new> <new><old>
    # Notes:
    #       This was going to be simple single pane swap, but decided to go for the same flexibility as rename
    #       Because of this, much of the code between rename and swap is the same or similar
    if not wg_PRIVATE:
        return flexsense['notices'].append( FlexError( "Please specify a window with use or new" ) )
    # This command could have wrapped join, but a native implementation has been made to reduce overhead somewhat
    wg = wg_PRIVATE
    used, unused = wg.Panes_GetUsedUnused()
    pairs = [ panes_from ] + [ arg for arg in panes_to ]
    if len(pairs)&1:
        return flexsense['notices'].append( FlexError( "Insufficient data, every <from> must be followed by <to>" ) )
    pairs = [ pairs[i*2:i*2+2] for i in range(len(pairs)>>1) ]
    # Check for errors
    swaplist = ""
    pair = "1"
    try:
        for f, t in pairs:
            # Pair counts must be equal
            if len(f) != len(t):
                raise Exception("Pair " + pair + " count error, both <from> and <to> pane counts must be identical")
            # Check for duplicates in the same spot of the same pair
            for spot, paneset in [ ("<from>", f), ("<to>", t) ]:
                paneid = ([paneid for paneid in paneset if paneset.count(paneid) > 1]+[None])[0]
                if paneid:
                    raise Exception("Pane `" + paneid + "` specified multiple times in " + spot + " of pair " + pair)
            # Check for self swap (this could be safely ignored)
            for fi, ti in zip(f, t):
                if fi == ti:
                    raise Exception("Pane `" + fi + "` swaps to self in pair " + pair)
            # Iterate all panes in this argument and validate
            for spot, paneid in zip( ["<from>" for _ in f] + ["<to>" for _ in t], f + t):
                if not paneid in PANE_CHARACTERS:
                    raise Exception("Invalid pane `" + paneid + "` in " + spot + " of pair " + pair)
                if paneid in swaplist: # Panes are only permitted to be swapped once
                    raise Exception("The " + spot + " pane `" + paneid + "` in pair " + pair + " is already swapped")
                if not paneid in used: # The pane must already be in use
                    raise Exception("The " + spot + " pane `" + paneid + "` in pair " + pair + " is not being used")
            # Next
            swaplist += f + t
            pair = str( int(pair) + 1 )
    except Exception as error:
        return flexsense['notices'].append( FlexError( str(error) ) )
    # Merge all arguments into a single unified from and to that contains both, so only one direction (f->t) is needed
    master_f, master_t = "".join([f for f, _ in pairs]), "".join([t for _, t in pairs])
    master_f, master_t = master_f + master_t, master_t + master_f
    # Perform the swaps in a single pass now that we know all panes are referenced only once
    windowgram_lines = wg.Export_Lines()
    wg.Import_Lines( [ "".join(
        [ ch if ch not in master_f else master_t[master_f.find(ch)] for ch in list(line) ]
        ) for line in windowgram_lines ] )
    # Replace windowgram
    wg_PRIVATE.Import_Wg( wg )

@flex(
    command     = "mirror",
    group       = "modifiers",
    description = "Reverse horizontally (left/right)",
)
def cmd_mirror(wg_PRIVATE):
    # TODO: Optional pane group mirror
    if not wg_PRIVATE:
        return flexsense['notices'].append( FlexError( "Please specify a window with use or new" ) )
    wg = wg_PRIVATE
    windowgram_lines = wg.Export_Lines()
    wg.Import_Lines( [ "".join( [ ch for ch in reversed(list(line)) ] ) for line in windowgram_lines ] )
    wg_PRIVATE.Import_Wg( wg )

@flex(
    command     = "flip",
    group       = "modifiers",
    description = "Reverse vertically (top/bottom)",
)
def cmd_flip(wg_PRIVATE):
    # TODO: Optional pane group flip
    if not wg_PRIVATE:
        return flexsense['notices'].append( FlexError( "Please specify a window with use or new" ) )
    wg = wg_PRIVATE
    windowgram_lines = wg.Export_Lines()
    wg.Import_Lines( reversed(windowgram_lines) )
    wg_PRIVATE.Import_Wg( wg )

##
## Commands: Terminators
##

@flex(
    command     = "oops",
    group       = "terminators",
    description = "Restore the original session, then exit without execution",
)
def cmd_oops():
    flexsense['finished'] = flexsense['restore'] = True

@flex(
    command     = "done",
    group       = "terminators",
    description = "Keep changes to session, then execute",
    aliases     = [ ["run", "done"], ["go", "done"] ],
)
def cmd_done():
    flexsense['finished'] = flexsense['execute'] = True

@flex(
    command     = "exit",
    group       = "terminators",
    description = "Keep changes to session, but do not execute",
    aliases     = [ ["x", "exit"] ],
)
def cmd_exit():
    flexsense['finished'] = True

##
## Flex Shell
##
## TODO: Reload the xterm dimensions before printing the buffer to support resize during use
## TODO: Support "again" that repeats the last command
##

def flex_shell(user_wh, session, serial=0):
    ##
    ## Print buffer
    ##
    leftgap = rightgap = 4
    buf = []
    def flexout(l):
        if l is None: buf.append( None )
        elif "\n" in l: return [ flexout(l) for l in l.split("\n") ]
        else: buf.append( (" " * leftgap) + str(l) )
    def flexout_divider():
        flexout( "-" * ( user_wh[0] - (leftgap + rightgap) ) )
    ##
    ## Session setup
    ##
    global flexmenu_session
    flexmenu_session = session
    session_original = copy.deepcopy(session) # Original copy
    ##
    ## Show list of windows, or assign selected window
    ##
    if serial is 0:
        cmd_list()
    else:
        flexmenu_index[0] = serial
        cmd_use(*[str(serial)]) # By calling this we assure blank windowgrams are properly initialized
    ##
    ## Input loop
    ##
    warnings = []
    queue = ""
    lastcmd = ""
    sc_support = None
    sc_serial = 0
    split_check = lambda: True \
        if not sc_serial or session.Get_Wg(sc_serial).Analyze_Type(ARGS.relative) == "split" else False
    while True:
        global flexsense
        label_w = 12
        labeler = lambda name: name + ( (" "*(label_w-len(name))) if len(name) < label_w else name ) + ": "
        if not flexmenu_session.Serial_Is_Valid(flexmenu_index[0]): flexmenu_index[0] = 0 # Serial is invalid, clear it
        # Macros
        string_to_list = lambda string: [ x.strip() for x in string.strip().split() ]
        filter_input = lambda string: ( string_to_list( string ), " ".join( string_to_list( string ) ) )
        # Multiple commands are expected to be without output
        if flexsense['output'] and queue:
            flexsense['notices'].append( FlexError( "Command \"" + lastcmd + "\" had output, " + \
            "commands with output interrupt multiple commands mode" ) )
        # Prepare for new command
        output = flexsense['output']
        warnings += flexsense['notices']
        # Check errors
        errors = True if [ 1 for warn in warnings if warn.GetLvl() ] else False
        # Flush queue if an error occurred
        if errors and queue:
            pending = queue.count(";") + (1 if len(queue) else 0)
            # Append to warnings accumulator, note that although this generates an error, there already was one
            warnings.append( FlexError( "Errors occurred, dropping " + str(pending) + \
                " pending command" + ("s" if pending-1 else "") ) )
            queue = ""
        # Shell header
        if not queue:
            flexout("")
            flexout("___ _   ___ _ _")
            flexout("__  _   __   _     Flex for tmuxomatic " + VERSION)
            flexout("_   ___ ___ _ _    The object-oriented windowgram editor")
            flexout("")
            flexout_divider()
            flexout("")
            flexout(None) # The fill marker used for later padding to keep header consistently on top
        # Always show windowgram as long as: the command produced no output, and no commands are enqueued
        if not flexsense['output'] and not queue:
            cmd_print()
        # Show output if there was any
        if flexsense['output']:
            line = ""
            for line in flexsense['output']:
                for line in line.split("\n"):
                    flexout(line)
            if line.strip():
                flexout("") # Force extra line at end if it does not exist
        # Divider
        if not queue:
            flexout_divider()
            flexout("")
        # Show warnings (only after queue is exhausted)
        if warnings and not queue:
            for warn in warnings:
                flexout( ( labeler("WARNING") if not warn.GetLvl() else labeler("ERROR") ) + warn.GetMsg() )
            warnings = []
            flexout("")
        # Show short command list in the context of a selection
        commands = flexmenu_grouped['helpers'] + flexmenu_grouped['selectors']
        if flexmenu_index[0]: commands = flexmenu_grouped['helpers'] + flexmenu_grouped['modifiers']
        if not queue:
            flexout(labeler("Quick Menu") + ", ".join(commands))
            flexout("")
        # Show selected window information
        if not queue:
            serial = flexmenu_index[0]
            if not serial:
                flexout( labeler("Window") + "None ... Try \"list\" or \"use <window>\"" )
            else:
                name = flexmenu_session.Get_Name(serial)
                wg = flexmenu_session.Get_Wg( serial )
                used, unused = wg.Panes_GetUsedUnused()
                flexout( labeler("Window") + "#" + str(serial) + " (" + name + ")" )
                flexout( labeler("Panes") + used + " < used " + str(len(used)) + " ... " + \
                    str(len(unused)) + " unused > " + unused )
            flexout("")
        # If the windowgram is unsupportable by tmux, the user should know
        # Example: "new unsupported ; break 1 3x3 1 ; join 12 36.2 98.3 74.4"
        if not queue:
            # If window changed, check the new window
            if not flexmenu_index[0]:
                sc_serial = 0
                sc_support = True
            elif sc_serial != flexmenu_index[0]:
                sc_serial = flexmenu_index[0]
                sc_support = split_check()
            # Notify user if window is incompatible with tmux
            if not sc_support:
                flexout( labeler("ATTENTION") + "This windowgram is not compatible with the split mechanics of tmux" )
                flexout("")
        # Display output
        if not queue:
            padding = user_wh[1] - len(buf) # Account for prompt
            if padding < 0: padding = 0
            for l in buf:
                if l is not None: print( l )
                elif padding: print( "\n" * (padding - 1) ) # Ignore otherwise
            buf = []
        # User input
        if not queue:
            try: thisinput_str = input("<<< tmuxomatic flex >>> ")
            except EOFError as e: thisinput_str = "exit" ; print("") # About to exit: print, not flexout
            if ";" in thisinput_str: queue = thisinput_str
        if queue:
            thisinput_str, queue = queue.split(";", 1) if ";" in queue else (queue, "")
            queue = " ; ".join( [ cmd.strip() for cmd in queue.split(";") if cmd.strip() ] )
        thisinput_lst, thisinput_str = filter_input( thisinput_str )
        lastcmd = thisinput_lst[0] if len(thisinput_lst) else lastcmd
        # Prepare for new command
        flexsense = copy.deepcopy( flexsense_reset )
        # Command specified
        if len(thisinput_lst):
            invoked = False
            # Ambiguity handler (repackages input)
            # This corrects the command or alias where possible, and reports ambiguity error otherwise
            # Eliminates the need for the manual entry of short aliases for flex commands
            # For example: "sp" -> "split"
            def AmbiguityMatch(part, whole): # True if part matches with whole[:part]
                if len(part) > len(whole): return False
                return False if [ True for p, w in zip(list(part), list(whole)) if p != w ] else True
            hits = []
            for alias_tup in flexmenu_aliases:
                of = alias_tup[0]
                if AmbiguityMatch( lastcmd, of ): hits.append( of )
            for cmd_dict in flexmenu:
                of = cmd_dict['about'][0]
                if AmbiguityMatch( lastcmd, of ): hits.append( of )
            if len(hits) == 1: lastcmd = hits[0]
            elif len(hits) > 1:
                flexsense['notices'].append( FlexError( "Ambiguous command \"" + lastcmd + "\" has " + \
                    str(len(hits)) + " matches: " + ", ".join(hits) ) )
                continue
            # Alias handler (repackages input)
            # Note that trailing space means duplicate parameters: ["?", "help "] forwards "? use new" to "help use new"
            for alias_tup in flexmenu_aliases:
                if alias_tup[0] == lastcmd:
                    newinput = alias_tup[1]
                    if newinput[-1:] == ' ': newinput += " ".join(thisinput_lst[1:]) # End space == duplicate arguments
                    thisinput_lst, thisinput_str = filter_input( newinput )
                    lastcmd = thisinput_lst[0] if len(thisinput_lst) else lastcmd
                    break
            # Command handler (based on provided arguments and first matching function)
            finished = False
            argcount = len(thisinput_lst) - 1
            for cmd_dict in flexmenu:
                if cmd_dict['about'][0] == lastcmd:
                    availability = [] # Available arguments if user error: [ [from, to], [from, to], ... ]
                    for ix, triplet in enumerate(usage_triplets(cmd_dict)):
                        usage, examples, arglens = triplet
                        group = cmd_dict['group'][ix]
                        if argcount >= arglens[0] and (argcount <= arglens[1] or arglens[1] == -1):
                            serial = flexmenu_index[0]
                            arguments = []
                            wg = None
                            if group == "modifiers":
                                if flexmenu_session.Serial_Is_Valid(serial): wg = flexmenu_session.Get_Wg(serial)
                                arguments.append( wg )
                            if argcount: arguments += thisinput_lst[1:]
                            cmd_dict['funcs'][ix]( *arguments )
                            if wg is not None:
                                flexmenu_session.Replace_Windowgram( serial, wg.Export_String() )
                            invoked = True
                            break
                    if not invoked:
                        # No invocation, could show available parameter counts, but showing help may be more useful
                        flexsense['notices'].append( FlexError( "Parameter mismatch for valid command \"" + \
                            lastcmd + "\", displaying help instead" ) )
                        cmd_help_N( lastcmd )
                        finished = True
                    break
            if finished: continue
            # Invalid command handler
            if not invoked:
                # Throw it in the warnings queue as an error and it will flush the queue on the next pass
                flexsense['notices'].append( FlexError( "Invalid command \"" + lastcmd + "\"" ) )
            # Save if session modified and print next pass
            if session.Modified():
                # TODO: Add to stack if command resulted in a modification
                session.Save()
                sc_support = split_check()
            # Finish handler
            if flexsense['finished']:
                if flexsense['restore']:
                    session = session_original
                    session.Save()
                if flexsense['execute']:
                    return session # Return object in case of restore
                exit()
        # Previous block assumes nothing follows, so it may continue to next command
    ##
    ## Not reached
    ##



##----------------------------------------------------------------------------------------------------------------------
##
## Processing (session file -> tmux commands)
##
##----------------------------------------------------------------------------------------------------------------------

def tmuxomatic( program_cli, full_cli, user_wh, session_name, session ):
    """

    Parse session file, build commands, execute.

    """

    # Show configuration
    if ARGS.verbose >= 1:
        print( "" )
        print( "(1) Session   : " + session_name )
        print( "(1) Running   : " + full_cli )
        print( "(1) Xterm     : " + str(user_wh[0]) + "x" + str(user_wh[1]) + " (WxH)" )
        print( "(1) Filename  : " + ARGS.filename )
        print( "(1) Verbose   : " + str(ARGS.verbose) + \
            " (" + ", ".join([ 'summary', 'inputs', 'fitting', 'commands' ][:ARGS.verbose]) + ")" )
        print( "(1) Recreate  : " + str(ARGS.recreate) )
        print( "(1) Noexecute : " + str(ARGS.noexecute) )
        print( "(1) Sizing    : " + [ "Absolute (characters)", "Relative (percentages)" ][ARGS.relative] )

    # Initialize
    list_execution = [] # List of tmux command lists for a session, only executed on successful parsing
    list_build = [] # Separate list per window
    window_serial = 0 # 1+
    window_name = ""
    window_names_seen = [] # Assert unique window names (related to issue #8)
    focus_window_name = None # Use window name rather than window index (supports tmux option: base-index)
    line = "" # Loaded line stored here

    #
    # Error reporting
    #
    errpkg = {}
    errpkg['command'] = program_cli
    errpkg['format'] = session.format
    errpkg['line'] = 0

    #
    # Reporting line numbers
    #
    def SetLineNumber(linebase, lineoffset):
        if errpkg['format'] == "shorthand":
            errpkg['line'] = linebase + lineoffset # Exact line (shorthand)
        else:
            errpkg['line'] = linebase # Approximate line (yaml)

    #
    # Parse session file
    #
    #   Each window:
    #
    #       1 = Initialize window
    #       2 = Windowgram parser
    #       3 = Build list_panes
    #       4 = Directions parser
    #       5 = Generate tmux commands
    #
    eof = False
    window = 0
    line = 0
    for window in session.windows:

        #
        # 1) Initialize window
        #
        title_lines = window.SplitCleanByKey('title')
        line = title_lines[0] if len(title_lines) else ""
        SetLineNumber( window.GetLines('title'), 0 )
        if not line or not is_windowdeclaration(line):
            synerr(errpkg, "Expecting a window section, found nothing")
        window_serial += 1 # 1+
        if window_serial > MAXIMUM_WINDOWS:
            synerr(errpkg, "There's a maximum of " + str(MAXIMUM_WINDOWS) + " windows in this version")
        window_process = line[6:].strip()
        window_name = "" # Window name enclosed in double-quotes
        window_name = "".join( [ ch if ch != '\"' else '\\"' for ch in window_process ] ) # Escape double-quotes
        if not window_name:
            synerr(errpkg, "Window serial " + str(window_serial) + " does not have a name")
        for ix, seen_name in enumerate(window_names_seen):
            if window_name == seen_name:
                synerr(errpkg, "As of version 2.0, window names must be unique.  The duplicate name, \"" + \
                    window_name + "\", for window " + str(window_serial) + ", already used by window " + str(1+ix))
        window_names_seen.append( window_name )
        if ARGS.verbose >= 2: print("")

        #
        # 2) Windowgram parser
        #
        windowgram_lines = window.SplitCleanByKey('windowgram')
        windowgram = Windowgram_Convert.Lines_To_String( windowgram_lines )
        wg = Windowgram(windowgram)
        if ARGS.verbose >= 2:
            print( "\n".join([ "(2) Windowgram: " + line for line in windowgram_lines if line ]) )
        layout, error, linenumber = Windowgram_Convert.String_To_Parsed(windowgram)
        if error:
            SetLineNumber( window.GetLines('windowgram'), linenumber - 1 )
            synerr(errpkg, "Windowgram parsing error for window serial " + str(window_serial) + ": " + error)
        # For every pane, add an initialized 'l' key that's used later for linking
        for pane in layout.keys(): layout[pane]['l'] = 0

        #
        # 3) Build list_panes
        #
        list_panes, layout = SortPanes( layout ) # Sort t to b, l to r, move into list (layout[] -> list_panes[])
        # Now check for overlaps
        overlap_pane1, overlap_pane2 = PaneOverlap( list_panes )
        if overlap_pane1 or overlap_pane2:
            synerr(errpkg, "Overlapping panes: " + overlap_pane1 + " and " + overlap_pane2)

        #
        # 4) Directions parser
        #
        default_directory = "" # Never set a default, assume the path that tmuxomatic was run from
        first_pdl = False # Verbose only
        for ix, line in enumerate(window.SplitCleanByKey('directions')):
            SetLineNumber( window.GetLines('directions'), ix )
            if not line: continue
            if ARGS.verbose >= 2:
                if not first_pdl: print("") ; first_pdl = True
                print("(2) Directions: " + line)
            if command_matches(line, "foc"):
                # Window focus
                focus_window_name = window_name
                continue # Next line
            if command_matches(line[:3], "dir"):
                # Default directory
                if ' ' in line or '\t' in line:
                    # Set or change the default directory.  Applies to successive panes until changed again.
                    values = line.split( None, 1 )
                    default_directory = values[1]
                continue # Next line
            # Splits the line into easier to handle strings, there's probably a better way to do this
            if not ' ' in line and not '\t' in line:
                synerr(errpkg, "Directions line syntax error")
            panedef_paneids, panedef_cmdplusargs = line.split( None, 1 )
            if not ' ' in panedef_cmdplusargs and not '\t' in panedef_cmdplusargs:
                panedef_cmd = panedef_cmdplusargs
                panedef_args = ''
            else:
                panedef_cmd, panedef_args = panedef_cmdplusargs.split( None, 1 )
            #
            # Make the list of targets from the specified panes
            #
            panelist = list(panedef_paneids)
            for paneid in panelist:
                if not paneid in PANE_CHARACTERS:
                    synerr(errpkg, "Directions pane id is outside of the supported range: [0-9a-zA-Z]")
            def into(key, value, mode=0): # 0 = Set, 1 = Set or append if present, 2 = Set or skip if present
                found = []
                for pane in list_panes:
                    if pane['n'] in panelist:
                        if mode == 0:
                            pane[key] = value
                        if mode == 1:
                            if key in pane: pane[key].append( value )
                            else: pane[key] = [value]
                        if mode == 2:
                            if not key in pane or not pane[key]: pane[key] = value
                        found.append( pane['n'] )
                delta = list(set(panelist) - set(found))
                if delta:
                    synerr(errpkg, "Pane(s) '" + "".join(delta) + "' were not specified in the windowgram")
            def all_panes_that_have_key(key):
                found = []
                for pane in list_panes:
                    if pane['n'] in panelist:
                        if key in pane:
                            found += [ pane['n'] ]
                return "".join(found)
            #
            # Target pane specified ... Set default directory if not already set for this pane
            #
            into('dir', default_directory, 2)
            #
            # Command handlers
            #
            if command_matches(panedef_cmd, "run"):
                if not panedef_args: synerr(errpkg, "Directions command 'run' must have arguments")
                into('run', panedef_args, 1)
            elif command_matches(panedef_cmd, "dir"):
                if not panedef_args: synerr(errpkg, "Directions command 'dir' must have arguments")
                into('dir', panedef_args)
            elif command_matches(panedef_cmd, "foc"):
                if panedef_args: synerr(errpkg, "Directions command 'foc' must have no arguments")
                panes = all_panes_that_have_key('foc')
                if panes: synerr(errpkg, "Directions command 'foc' already specified for panes: " + panes)
                into('foc', True)
            else:
                synerr(errpkg, "Unknown command '" + panedef_cmd + "'")

        #
        # 5) Generate tmux commands ... After splitting and cross-referencing
        #

        #
        # 5.1) Refine list_panes so all expected variables are present for cleaner reference
        #
        for pane in list_panes:
            if not 'dir' in pane: pane['dir'] = ""
            if not 'run' in pane: pane['run'] = [ "" ]
            if not 'foc' in pane: pane['foc'] = False

        #
        # 5.2) Split window into panes
        #
        if ARGS.verbose >= 3:
            print("")
            print("(3) Fitting panes = {")
        sw = { 'print': print, 'verbose': ARGS.verbose, 'relative': ARGS.relative, 'scanline': DEBUG_SCANLINE } # Print
        list_split, list_links = SplitProcessor( sw, wg, user_wh[0], user_wh[1], list_panes )
        if ARGS.verbose >= 3:
            print("(3) }")

        #
        # 5.3) Build the execution list for: a) creating windows, b) sizing panes, c) running commands
        #
        list_build = [] # Window is independently assembled

        #
        # 5.3a) Create window panes by splitting windows
        #
        first_pane = True
        for split in list_split:
            #
            # Readability
            #
            list_split_linkid = split['linkid']     # 1234          This is for cross-referencing
            list_split_orient = split['split']      # "v" / "h"     Successive: Split vertical or horizontal
            list_split_paneid = split['tmux']       # 0             Successive: Pane split at time of split
            list_split_inst_w = split['inst_w']     # w             Successive: Ensuing window size in chars
            list_split_inst_h = split['inst_h']     # h             Successive: Ensuing window size in chars
            list_split_percnt = split['per']        # 50.0          Successive: Percentage at time of split
            ent_panes = ''
            for i in list_panes:
                if 'l' in i and i['l'] == list_split_linkid:
                    ent_panes = i
                    break
            if not ent_panes:
                SetLineNumber( window.GetLines('windowgram'), 0 )
                synerr(errpkg,
                    "Unable to fully cross-link.  This is because of an unsupported window layout.  See the " + \
                    "included example file `session_unsupported` for more information on what layouts are and " + \
                    "aren't possible in tmux.  If you use flex to generate windowgrams, it will notify you as soon " + \
                    "as you create a pane layout that is not supported by tmux.  For more information, look up the " + \
                    "clean split rule in the tmuxomatic documentation.")
            list_panes_dir = ent_panes['dir']       # "/tmp"        Directory of pane
            if list_panes_dir: adddir = " -c " + list_panes_dir
            else: adddir = ""
            #
            # Add the commands for this split
            #
            if first_pane: # First
                first_pane = False
                if window_serial == 1:
                    # First pane of first window
                    # The shell's cwd must be set, the only other way to do this is to discard the
                    # window that is automatically created when calling "new-session".
                    cwd = "cd " + list_panes_dir + " ; " if list_panes_dir else ""
                    list_build.append(
                        cwd + EXE_TMUX + " new-session -d -s " + session_name + " -n \"" + window_name + "\"" )
                    # Normally, tmux automatically renames windows based on whatever is running in the focused pane.
                    # There are two ways to fix this.  1) Add "set-option -g allow-rename off" to your ".tmux.conf".
                    # 2) Add "export DISABLE_AUTO_TITLE=true" to your shell's run commands file (e.g., ".bashrc").
                    # Here we automatically do method 1 for the user, unless the user requests otherwise.
                    list_build.append( EXE_TMUX + " set-option -t " + session_name + " quiet on" )
                    renaming = [ "off", "on" ][ARGS.renaming]
                    list_build.append( EXE_TMUX + " set-option -t " + session_name + " allow-rename " + renaming )
                    list_build.append( EXE_TMUX + " set-option -t " + session_name + " automatic-rename " + renaming )
                else:
                    # First pane of successive window
                    list_build.append( EXE_TMUX + " new-window -n \"" + window_name + "\"" + adddir )
            else: # Successive
                # Perform the split on this pane
                list_build.append( EXE_TMUX + " select-pane -t " + str(list_split_paneid) )
                # Pane sizing
                if ARGS.relative:
                    # Relative pane sizing (percentage)
                    percentage = str( int( float( list_split_percnt ) ) ) # Integers are required by tmux 1.8
                    list_build.append( EXE_TMUX + " split-window -" + list_split_orient + " -p " + percentage + adddir )
                else:
                    # Absolute pane sizing (characters)
                    if list_split_orient == 'v': addaxis = " -y " + str( list_split_inst_h )
                    else: addaxis = " -x " + str( list_split_inst_w )
                    list_build.append( EXE_TMUX + " split-window -" + list_split_orient + adddir )
                    list_build.append( EXE_TMUX + " resize-pane -t " + str(list_split_paneid + 1) + addaxis )

        #
        # 5.3b) Prepare shell commands ... This is done separately after the pane size has been established
        #
        for ent_panes in list_panes:
            # Now that the tmux pane index correlates, cross-reference for easier lookups
            list_panes_l = ent_panes['l']           # 1234          This is for cross-referencing
            ent_panes['tmux'] = str([tup[1] for tup in list_links if tup[0] == list_panes_l][0])
        focus_actual_tmux_pane_index = "0" # Default pane_index
        for ent_panes in list_panes:
            #
            # Readability
            #
            list_panes_l = ent_panes['l']           # 1234          This is for cross-referencing
            list_panes_run = ent_panes['run']       # ["cd", "ls"]  Commands to run on pane
            list_panes_foc = ent_panes['foc']       # True          Determines if pane is in focus
            list_panes_index = ent_panes['tmux']
            #
            # Run
            #
            if list_panes_run:
                for run in list_panes_run:
                    clean_run = re.sub(r'([\"])', r'\\\1', run) # Escape double-quotes
                    if clean_run:
                        list_build.append( EXE_TMUX + " select-pane -t " + list_panes_index )
                        list_build.append( EXE_TMUX + " send-keys \"" + clean_run + "\" C-m" )
            if not focus_actual_tmux_pane_index or list_panes_foc:
                focus_actual_tmux_pane_index = list_panes_index
        if focus_actual_tmux_pane_index:
            list_build.append( EXE_TMUX + " select-pane -t " + focus_actual_tmux_pane_index )

        #
        # 5.4) Add this batch to the main execution list to be run later
        #
        list_execution.append( list_build )

        #
        # Done
        #

    #
    # Set default window
    #
    if focus_window_name is not None:
        list_build.append( EXE_TMUX + " select-window -t \"" + focus_window_name + "\"" )

    #
    # Notify user that tmux execution will begin and allow for time to break (ARGS.verbose >= 1)
    #
    if ARGS.verbose >= 1:
        print("")
        if VERBOSE_WAIT != 0:
            print("(1) Waiting " + str(VERBOSE_WAIT) + " seconds before running tmux commands...")
            time.sleep(VERBOSE_WAIT)
        print("(1) Running tmux commands...")
        print("")

    #
    # Run the tmux commands
    #
    for block in list_execution:
        for command in block:
            error = tmux_run(command)
            if error:
                if "pane too small" in error:
                    errpkg['quiet'] = True
                    msg = "Window splitting error (pane too small), make your window larger and try again"
                else:
                    msg = "An error occurred in tmux: " + error
                synerr(errpkg, msg )

    #
    # Attach to the newly created session
    #
    tmux_run( EXE_TMUX + " attach-session -t " + session_name )



##----------------------------------------------------------------------------------------------------------------------
##
## Main (tmuxomatic)
##
##----------------------------------------------------------------------------------------------------------------------

def main():

    # Verify pane count
    if MAXIMUM_PANES != 62 or len(PANE_CHARACTERS) != MAXIMUM_PANES:
        print("Pane count does not match")
        exit(0)

    # Check tmux version (req = required, rep = reported)
    tmux_req = MINIMUM_TMUX
    tmux_cli, tmux_rep = tmux_version()
    if tmux_cli != "tmux" or not tmux_rep:
        print("The tmux executable cannot be found")
        exit(0)
    if not satisfies_minimum_version( tmux_req, tmux_rep ):
        print("This requires tmux " + tmux_req + " or higher, found tmux " + tmux_rep)
        exit(0)

    # Settings
    program_cli = sys.argv[0]                   # Program cli: "./tmuxomatic"
    user_wh = get_xterm_dimensions_wh()         # Screen dimensions

    # Constrain arguments
    ancillary = False # Used with printonly and scale, to skip over the main tmuxomatic functionality
    ARGS.verbose = int(ARGS.verbose or 0)
    if ARGS.verbose > VERBOSE_MAX: ARGS.verbose = VERBOSE_MAX
    elif ARGS.printonly:                        # Overrides for --printonly
        ancillary = True
        ARGS.noexecute = False
        ARGS.verbose = 0

    # If using flex and a serial was specified
    serial = 0
    if ARGS.flex and ":" in ARGS.filename:
        ARGS.filename, serial = ARGS.filename.split(":", 1)
        if not serial.isdigit():
            print("You specified a flex window serial that does not make sense: " + serial)
            exit(0)
        serial = int(serial)

    # Check for presence of specified session filename
    if not os.path.exists(ARGS.filename):
        if ARGS.flex:
            f = open(ARGS.filename, 'w')
            line = "##" + "-" * 78
            f.write( line + "\n##\n## Session file created by tmuxomatic flex " + VERSION + "\n##\n" + line + "\n\n" )
            f.close() # Required for proper updating on first new window
        else:
            print("The specified session file does not exist: " + ARGS.filename)
            exit(0)

    # Make sure the session file is not unexpectedly large (say the user accidentally specified a binary file)
    if 2**20 < os.stat(ARGS.filename).st_size:
        print("The specified session exceeds 1 megabyte, that's nearly 1 megabyte more than expected.")
        exit(0)

    # Session name in tmux is always derived from the filename (pathname is dropped to avoid confusion)
    filename_only = ARGS.filename[ARGS.filename.rfind('/')+1:] # Get the filename only (drop the pathname)
    session_name = PROGRAM_THIS + "_" + filename_only # Session name with the executable name as a prefix
    session_name = re.sub(r'([/])', r'_', session_name) # In case of session path: replace '/' with '_'
    session_name = re.sub(r'\_\_+', r'_', session_name) # Replace two or more consecutive underscores with one

    # Load session file
    session = SessionFile( ARGS.filename )
    session.Load()
    new_name = session.RenameIfSpecified()
    if new_name is not None: session_name = new_name

    # Flex shell entry
    if ARGS.flex:
        session = flex_shell( user_wh, session, serial )
        # Force reload of session file in order to get accurate line counts in the event of changes by user in flex
        session.Load()

    # Optional kill session on disconnect
    def destroy():
        if ARGS.destroy:
            tmux_run( EXE_TMUX + " kill-session -t " + session_name, nopipe=True, force=True, real=True )

    # Existing session handler (skipped when printing or scaling)
    if not ancillary:
        # Detect existing session
        result = tmux_run( EXE_TMUX + " has-session -t " + session_name, nopipe=False, force=True, real=True )
        if not result:
            # Handle existing session
            if ARGS.recreate:
                # Destroy existing session (optional)
                print("Destroying running session, \"" + session_name + "\"...")
                tmux_run( EXE_TMUX + " kill-session -t " + session_name, nopipe=False, force=False, real=True )
            else:
                # Attach existing session
                print("Attaching running session, \"" + session_name + "\"...")
                try:
                    tmux_run( EXE_TMUX + " attach-session -t " + session_name, nopipe=True, force=False, real=True )
                except KeyboardInterrupt: # User disconnected
                    destroy()
                exit(0)

    # If printing, display header
    if ARGS.printonly:
        print("###")
        print("### Session \"" + session_name + "\"")
        print("### Generated by tmuxomatic for static configurations")
        print("### Using screen dimensions: " + str(user_wh[0]) + "x" + str(user_wh[1]) + " (WxH)")
        print("###")

    # Process session: generates a new session and attaches, or prints, or scales
    if not ancillary: print("Running new session, \"" + session_name + "\"...")
    try:
        tmuxomatic( program_cli, " ".join(sys.argv), user_wh, session_name, session )
    except KeyboardInterrupt: # User disconnected
        destroy()
    exit(0)



##----------------------------------------------------------------------------------------------------------------------
##
## Main (python)
##
##----------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":

    # Signal handlers
    signal.signal(signal.SIGINT, signal_handler_break) # SIGINT (user break)
    signal.signal(signal.SIGHUP, signal_handler_hup) # SIGHUP (user disconnect)

    # Argument deprecations
    for arg in sys.argv[1:]:
        dep = [ [ "Argument " + arg + " removed in version " + version + ": " + reason ] \
            for version, reason, commands in [
            [ "1.0.20", "Absolute positioning enabled by default", [ "-a", "--absolute" ] ],
            [ "2.0",    "Use --flex to scale your windowgrams",    [ "-s", "--scale" ] ],
            [ "2.0",    "Use --flex for windowgram modification",  [ "-w", "--scale-replace" ] ],
            ] if arg in commands ]
        if dep:
            print("!!! " + dep[0][0])
            skip = True
    if 'skip' in vars() and skip is True:
        print("Exiting...")
        exit()

    # Argument parser
    PARSER = argparse.ArgumentParser( description=\
        "The easiest way to define sessions in tmux! ... An introduction and example " + \
        "sessions are on the project home page: " + HOMEPAGE )
    PARSER.add_argument( "-V", "--version", action="version", version=PROGRAM_THIS + " " + VERSION, help=\
        "Show the version number and exit" )
    PARSER.add_argument( "-v", "--verbose", action="count", help=\
        "Increase the verbosity level, up to " + str(VERBOSE_MAX) + " (-" + (VERBOSE_MAX * 'v') + ")" )
    PARSER.add_argument( "-n", "--renaming", action="store_true", help=\
        "Let tmux automatically rename the windows" )
    PARSER.add_argument( "-p", "--printonly", action="store_true", help=\
        "Print only the tmux commands, then exit" )
    PARSER.add_argument( "-x", "--noexecute", action="store_true", help=\
        "Do everything except issue commands to tmux" )
    PARSER.add_argument( "-r", "--recreate", action="store_true", help=\
        "If the session exists, it will be destroyed then recreated.  " + \
        "Normally, if it exists, tmuxomatic will reattach to it.")
    PARSER.add_argument( "-d", "--destroy", action="store_true", help=\
        "When you disconnect, your session will be destroyed.  This " + \
        "is useful in situations where you don't want to consume " + \
        "resources when you're not 'plugged in'." )
    PARSER.add_argument( "-f", "--flex", action="store_true", help=\
        "Flex is an object-oriented windowgram editor.  It allows you " + \
        "to bend your windowgrams to perfection using visually " + \
        "oriented commands (scale, break, etc).  If you know which " + \
        "window you'll edit, add \":<number>\" after the filename." )
    PARSER.add_argument( "filename", help=\
        "The tmuxomatic session filename (required)" )
    ARGS = PARSER.parse_args()

    # Only absolute placement is supported in this version, relative placement could be useful for programs like weechat
    ARGS.relative = False

    # Locate tmux
    EXE_TMUX = which( EXE_TMUX )
    if not EXE_TMUX:
        print("This requires tmux to be installed on your system...")
        print("If it's already installed, update your $PATH, or set EXE_TMUX in the source to an absolute filename...")
        exit(0)

    # Run tmuxomatic ... A separate function was needed to quiet pylint (local variable scope)
    main()



