" File: VHDL instantiation script for VIM
" Author: e.shpack@gmail.com 
" Description: 
" Last Modified: Tue 25 Mar 2014 07:40:34 PM
"
command! -nargs=1  -complete=file InstVHDL call InstVHDL('<args>')

let s:srcFilePath = expand('<sfile>:p:h')

function! InstVHDL(fileName)
  let instFileName = fnamemodify(a:fileName, ':p')
  let currBufferFileName = expand("%:p")
  let currLineNumber = line('.')
  
  execute 'w'

  let pathToInstatiationScript = s:srcFilePath . '/instVHDL.py'
  let commandLineInterfaceCommand = 'python ' . '"' . pathToInstatiationScript .'" "' .instFileName . '" "'.currBufferFileName .'" ' . currLineNumber
  let systemOut = system(commandLineInterfaceCommand)
  
  execute 'e'
	
  echo systemOut
endfunction 
