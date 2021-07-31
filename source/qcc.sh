_Question()
{
	local cur=${COMP_WORDS[COMP_CWORD]}
	COMPREPLY=( $(compgen -W "show claim hang comment history report news") $cur )
}
complete -F _Question Question
