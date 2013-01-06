#!/usr/bin/python
# -*- coding: utf-8 -*-


import re


# --------------------------------------------------------------------------- #
#                                                                             #
#    Plugin for iSida Jabber Bot                                              #
#    Copyright (C) 2012 Alexey V Zapparov AKA ixti <ixti@member.fsf.org>      #
#                                                                             #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License, or        #
#    (at your option) any later version.                                      #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU General Public License for more details.                             #
#                                                                             #
#    You should have received a copy of the GNU General Public License        #
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.    #
#                                                                             #
# --------------------------------------------------------------------------- #


head_tpl = string.Template(u"* $name  ~  ☆$watchers_count  ⋌$forks_count\n*\n")
body_tpl = string.Template(u"* $description\n* $html_url")


def format_msg(data):
  return head_tpl.substitute(data) + body_tpl.substitute(data)


def github(type, jid, nick, text):
  msg, text = '', text.strip()

  if text:
    try:
      data = html_encode(load_page('https://api.github.com/repos/' + text))
      data = json.loads(data)
      msg  = "\n" + format_msg(data)

    except:
      msg = L('Repo \"%s\" not found!') % text

    send_msg(type, jid, nick, msg)


github_link_re = re.compile('github\.com/([^/ ]+)/([a-z0-9_~\-]+)(?:[^a-z0-9_~\-]|$)', re.IGNORECASE)


def fetch_github_links(room, jid, nick, type, text):
  if Settings['nickname'] == nick:
    return False

  match = github_link_re.search(text)

  if match:
    try:
      repo = "%s/%s" % match.groups()
      data = html_encode(load_page('https://api.github.com/repos/' + repo))
      data = json.loads(data)
      msg  = format_msg(data)

      send_msg(type, room, "", "\n" + msg)
      return True

    except:
      None

  return False


def git_manage(type, jid, nick, text):
  send_msg(type, jid, nick, "Not implemented yet")


global execute, message_act_control

message_act_control = [fetch_github_links]
execute             = [
    (3, 'github', github, 2, L('Show github project')),
    (9, 'git', git_manage, 2, L('Monitor git changes.'))]

