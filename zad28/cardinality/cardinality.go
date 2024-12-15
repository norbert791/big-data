package cardinality

type Cardinality interface {
	Add(uint32)
	Count() uint64
}
