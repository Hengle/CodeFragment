from pyquery import PyQuery as pq
d=pq(url='http://fenxi.zgzcw.com/1768039/bfyc')
left=d('div').filter('.bfyc-only-left')('tr').eq(1)('td')
print(left.eq(0).text());
print(left.eq(1).text());


