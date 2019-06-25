(set-logic QF_S)

(declare-fun v0 () String)
(declare-fun v1 () String)

(assert (str.contains v0 "thequickbrownfox"))
(assert (str.contains v0 v1))
(assert (str.contains "jumpsoverthelazydog" v1))

(assert (= 6 (str.len v1)))
(check-sat)
(get-model)