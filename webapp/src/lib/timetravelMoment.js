// moment does not let us clone and only locally override `now`
// we need to get a clean instance to manipulate
delete require.cache[require.resolve('moment')]
var moment = require('moment')
delete require.cache[require.resolve('moment')]

moment.now = function () { return 1587201480000 }
export default moment