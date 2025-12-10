EYE := ../../tools/eye/bin/eye

answer.n3: token.n3 logic.n3 population.n3 allen.n3 eventTime_rules.n3
	./$(EYE) \
	--quiet \
	--skolem-genid 8b98b360-9a70-4845-b52c-c675af60ad01 \
	--nope \
	$^ \
	--query query.n3 \
	--output $@
