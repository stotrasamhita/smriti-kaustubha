--[[ Pandoc Lua filter: text-model spans and divs (made by tools/build_pdf.py from the Hugo
shortcodes) → LaTeX macros defined in pdf/sk.latex. Spec §7. ]]

local function raw(s) return pandoc.RawInline("latex", s) end

local function esc(s)
  return (s:gsub("[\\{}#$%%&_^~]", function(c)
    local map = { ["\\"] = "\\textbackslash{}", ["^"] = "\\textasciicircum{}", ["~"] = "\\textasciitilde{}" }
    return map[c] or ("\\" .. c)
  end))
end

local function wrap(pre, inlines, post)
  local out = pandoc.List({ raw(pre) })
  out:extend(inlines)
  out:insert(raw(post))
  return out
end

function Span(el)
  local c = el.classes
  if c:includes("pg") then
    return raw("\\skpg{" .. pandoc.utils.stringify(el.content) .. "}")
  elseif c:includes("corr") then
    -- Our correction: print the corrected text, record the OCR reading in apparatus series A.
    return wrap("\\skcorr{", el.content, "}{" .. esc(el.attributes.ocr or "") .. "}")
  elseif c:includes("em") then
    return wrap("\\skem{", el.content, "}{" .. esc(el.attributes.print or "") .. "}")
  elseif c:includes("var") then
    return wrap("\\skvar{", el.content, "}")
  elseif c:includes("mn") then
    return wrap("\\skmn{", el.content, "}")
  elseif c:includes("doubt") then
    return raw("\\skdoubt{}")
  elseif c:includes("q") then
    return wrap("\\skq{" .. (el.attributes.src or "") .. "}{", el.content, "}")
  end
end

function Div(el)
  if el.classes:includes("shloka") then
    local lines = pandoc.List()
    for _, blk in ipairs(el.content) do
      if blk.t == "LineBlock" then
        for i, ln in ipairs(blk.content) do
          -- Half-verses in pairs: the second line of each pair is indented.
          local l = pandoc.List({ raw(i % 2 == 0 and "\\skindent " or "") })
          l:extend(ln)
          l:insert(raw(i < #blk.content and "\\\\\n" or ""))
          lines:extend(l)
        end
      end
    end
    local out = pandoc.List({ raw("\\begin{skshloka}{" .. el.identifier .. "}\n") })
    out:extend(lines)
    out:insert(raw("\n\\end{skshloka}"))
    return pandoc.Plain(out)
  elseif el.classes:includes("para") then
    local blocks = el.content
    if #blocks > 0 and blocks[1].t == "Para" then
      blocks[1].content:insert(1, raw("\\skpara{" .. el.identifier .. "}"))
    end
    return blocks
  end
end

function Header(el)
  if el.level == 1 then
    local url = el.attributes.url or ""
    local status = el.attributes.status or ""
    return pandoc.Plain(wrap("\\sktopic{" .. el.identifier .. "}{" .. url .. "}{" .. status .. "}{",
      el.content, "}"))
  end
end
