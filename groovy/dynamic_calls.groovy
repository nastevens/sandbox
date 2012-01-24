class BaseTest {

    def getProperty(final String name) {
        println "Property: $name"
    }

    def invokeMethod(final String name, args) {
        println args?.class
        println "Method: $name"
    }
}

class PropertyTest extends BaseTest {

    def call(Object[] args) {
        println "Called with ${args.size()} arguments"
    }

    def someMethod() {
        println "Called someMethod"
    }
}

p = new PropertyTest()
p.a { println "Glee" }
p.b
p.c()
p['b']
p 1, 2
p.someMethod()
