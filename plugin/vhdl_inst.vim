
command! -nargs=1  -complete=file VHDLinst call VHDLinst('<args>')

function! VHDLinst(fileName)
  let instFileName = fnamemodify('a:fileName', ':p')
  let currBufferFileName = expand("%")
  let currLineNumber = line('.')
  let currDir = getcwd()
  execute 'w'
"  Path to script declaration
  if has('win32') 
	let pathToInstatiationScript = $HOME . 'vimfiles\plugin\instantiateEntityVHDL.py'
  else
	let pathToInstatiationScript = '~/.vim/plugin/instantiateEntityVHDL.py'
  endif 
  if has('win32') 
	let pathToInstatiationScript = $HOME . 'vimfiles\plugin\instantiateEntityVHDL.py'
	let commandLineInterfaceCommand = 'python ' . '"' . pathToInstatiationScript .'"' . ' ' . '"' .instFileName . '"' .' ' . '"'.currDir.'\' .currBufferFileName .'"' . ' ' . currLineNumber
  else
	let pathToInstatiationScript = '~/.vim/plugin/instantiateEntityVHDL.py'
	let commandLineInterfaceCommand = 'python ' . pathToInstatiationScript . ' ' . instFileName . ' '.currDir . currBufferFileName . ' ' . currLineNumber
  endif
  call system(commandLineInterfaceCommand)
  execute 'e'
endfunction 
