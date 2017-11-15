from app import dkim_dmarc_proxy
domain1='email.tthigo.com'
license1='tthigo.webpower.asia'
domain2='e1.starbucks.com.cn'
license2='starbucks.webpower.asia'
domain3='e2.starbucks.com.cn'
license3='starbucks-system.webpower.asia'
domain4='starbucks-system.webpower.asia'
license4='e2.starbucks.com.cn'
domain5='service.toursforfun.com'
license5='toursforfun-service.dmdelivery.com'
domain6='my-edm.toysrus.com.my'
license6='toysrusmy.webpower.eu'



dkim_dmarc_proxy.new_dkim_dmarc(domain2,license2)