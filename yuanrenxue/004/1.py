import base64
import hashlib
import re
import sys

import httpx

url = "https://match.yuanrenxue.cn/api/question/4"

base64_to_num = {
    'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABkAAAAfCAYAAAASsGZ+AAACv0lEQVR4nNWWT0iTYRjAf5tzU9f8l59ojEjMSCMwglqHHEHsphANL3ryEHQICgIPngsMD4EHQWgQFJ1DDFmELDqMLlIHD9UMbNbom9OcNvf366K57X2+qYSHntv3fO/7/N73ed7nj6WwETM4YrEeNQDAtu+K/AZr4SAb70JklyMYegRcHixaJ9WXvdRf89LUWNmEpZK71ufHiT8JYGQqmXBj9U/SfrOHuqpDQdLEA7dYmwtXPmKxoUvTaPe8NAggMSa/5sYOBQAw3t8iPhelIPxTIXqQxLMZdWWND/vINI2jT3H5/VgEY4UXAX6uq3ol8KuvpsiVx8Dej/PRBCfadr4vekid0Vh5OEWJrzPP2Xo7AgPuCjfZDrP5elE5iXXw7h5gR2p7h6jrEm7zMkiifH/JQRZCZJSX5KP2irtcCWi4rvpUdXKB7VgFyGZECHabl1pNYACuHq8QmyCZr2kziE76k+oqujtpkBnQ6hazOZ/QzSHZJXWDRdPMa0+NQ/xX+GEGyafFzLYcc5ghADc2IfhkKcmXPUgiSq6CuUNJNMqWCDlC+Y8hrRrFkdyD1NRjUqkrSBojKaidDuwixFUvXsuI64J2V3TyMVVrbS/N3iK7GrZTAmR1A9OetaqTF9RVzaYQN9Udwo6Pi2yaMArfFoVn78N+ujS3SjzkPDekWkqGSC3LkLUPIVUp1LoSSF33BSEuYVKzC6TK1VthklJbuO6hqVxX8qV5cfaqJdeYv0Nstqgi5KN8H79PVmluQzj71LagDBKFzwGWxsYRRxiXB4sTjEQY6TVYB9/Q4Xcr3lC8Y+0a4fiw0IwAkmGMmAzg7AQtN1SACAFoGpigecArgyQ5/4CW0X5xHIJ9hrvfSzPok4/JrETlBa5+7MO30fo6TQe7fSG7ktvWSX6JkPvbVR3YTvbg0hwHmHMPCPlX+QOdeepDgNxkwQAAAB10RVh0dgB1Mjk0MC1wMS02LTllNTU3YjI4OTI1ZjVmOTXIz9qJAAAAAElFTkSuQmCC': 0,
    'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABkAAAAfCAYAAAASsGZ+AAAA0ElEQVR4nGP89+nFfwYaAyZaW8DAwMDAQo6mP093MTxpa2L4/fo1VMSNgXvqZAYpUWpY8vc1w+slTQwftu4iSRtRlvz79Zrh7YYJDB83rWH4/4sk8wlY8vcnw8eruxg+bt/M8PPsQdJNJsaSz7tLGF7NIy1YcAG6pC7SLOEIYeAKiSbZEuJSF68vA1tMEoOInRYD99XpDLepZQmzjD0DR1IIA7eBBYOABDtF4YrTEi6dEAYuHQpMRgKDMOJHLRm1ZNSSUUtGLRm1BDtgHDYNbgBRgjXoqop7sgAAAB50RVh0dgB1Mjk0MC1wMS0xMi01OTE4YzZmYzcxYWQxYWVi4RNGjQAAAABJRU5ErkJggg==': 1,
    'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABkAAAAfCAYAAAASsGZ+AAACe0lEQVR4nL2WPWhTURTHf2nS92I/Ym18YGkIQtEhgyiIpBTMUro5CA6CQzBDJUi1Q7C0SMBFSOkQ6CC4dLG4BEWLIHWKInQotFQILq0ffQ2F2Jo2jfalfS8uDkneTfL6lTOe/733d++555x7bcb2epETtqaTBgA4aqq6xtZKkp1PCxQWU+i7KsWsCu1+bK0emnv9tPQGOHPeVXMhmyhcRk7l16s4Wx9moGBhq90h2iIjdHVbhWzM8u3hEPtWFi81yY/86DneS7JJMt+JoWEcFABQmEMbj7GeNUu17wRA6sF2MYDkUf47MuifZ9jPZQSgaXbe3MII+sp2Xx3iHEC+N4zb30OrvUILhslMDZKdXTBNK36cIxv00VniE6aw/dokytQk3j4BAMDuQrkbxdku0HIptI1yl/kknTfwRiwUkN1Dcw/sLlYKGkWj3GNey261QmWaWi0NPErFL6MtifweHBVhPDSksJREywmECz5OOY8Dkl9g/VkcUWd19AeozIeDQ3SVdGzIlEEAuEc4fd1lch8IYuRSrI7eJv9VUIgEaBkN0SlIecuQPysJfty/ye53EeAK8tgEXV7x3PptRd9m812MjRcJsS75kSOTeC67qu64znuikn4aJP9FFetKiLax6i2+PiSfYvXJYJXwKNh6o5x9MECHqO1Ygugq6VgVgORHCk/Q3adYiHUNyObLiDiD3HdoexytG576kLUEv9+aWzjuYTrGwyiizlvHKhJCI/M6jmEa5kMOhw4FgMqT6Cn+zokv2pif5ue8tUWl/hDnSmqmHLK2TEH4vifZe5+0RgC4GoISSHm4shlh0zuqNeQH2RCI8Ad53NaQk/wDUOnJokC7XfIAAAAedEVYdHYAdTI5NDAtcDEtNzAtMDg3ODdhMDk5OTQxYmEyNSxt1UQAAAAASUVORK5CYII=': 2,
    'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABkAAAAfCAYAAAASsGZ+AAACrElEQVR4nLWWT0iTcRjHP0t9p1Onpm9YLomEkP4I4mXDaJcSL7vtEBgIu3koJkkegkEdAiNKT0EHwcNOdQi8SH8OO0gjiMmIDsYqbOrwxWHvttwft3Voie79vdtc83t8nuf9fd7f7/k93/c15NRInmPWieMGANTrJfaSYdQPfuLBAOlQGBIh8jEF2q0YGi002KyYbHY6zpn1FynIoD2uMJuP7hNf8Vf2mj0uWqamOd2jXyI4LoVMpQCA9XnikzdZC6aOAqlGAVKPZ4jsiLMljlOG3hGM1+00yca/oaTCru8VKdFO017i71zgtFQGMVz20D4xhiwLksMOfn+aZWPmOcV3Px/8QtxpoaUoLjiuQc56dAAFmYacNHULEtmUBqwDqUQWjAOVV1cJUdnbEoRPyRhrBclFfCRWiqMykm0QSVBfblg1SnxdRHk6Ra440T9N+5BoH6Ug2z5+PJhn70AoH/VDWlAru+mYdtBWJ15KH5JTyUb8wtuyr1YH0q0J5Gt9mHQA8D8TL9lpGLZitJQ3yCP3ZF9pH5klH5kliMkumu+6OXNe3BOBCxcUC7DxMnCgJyq5VT+ZbwExVLJivPeC3gEtSB+ip6xK9O0s0Xmvtl+dbjqeTdDVeDh89J7UmTk56kF2ObS57VniH1VNuOrGt90YEw5eZjVUOwh1YKiwtHpIMqWd+sogIZRl5dCU6+nXey8ZQby+V/vRKoKo7M5d5fvkQ34uh4gLLCSXVlAWbrO18EaAsCNd0n6IxMO47iU552UToNWKobkQT4bJ74SFjwAYRt3Igr+W8hMf85OPla2C/ifI4xdrY/VayRhsHrrujOi6sGbiY8FFoq+9pD/r2Mc/SX2cuDKGedxJZ7ex5DXVt5Vsit1omMSaUmQfZqQLFppMZqQS9l4ZpIb6A1fu5S14k/1FAAAAHnRFWHR2AHUyOTQwLXAxLTExLTVkNTMyNzFiMmNjNjBhYTbu44FuAAAAAElFTkSuQmCC': 3,
    'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABkAAAAeCAYAAADZ7LXbAAABz0lEQVR4nO2WMUvDUBSFT2qttaJCazBg0cmlTkE3R6F0cauz2MVJcCh0KCh2E9wEiw4VBH+AFBwCDoq4VlBLQXAItQYT0bamkKiJg9amSdW+EDt5tnvIzZeXk5d3Ka0i6Phjue21KShf5qAqza5rhEWA6XEIInKQUnFoJtsVO0UgQlsud5ETFEgHGQvgJxFDND6LMpcn6iGEiBC2k0SrIIbIJ2nI14QEIsjTMcSdfXJC+5AKhK0kXtR6TQMehyFVLoXqudgwRpfhm3YQoglZSHtZg8PCuxhFT7dTkLci7jbieFUbFhVZwfB4+4BfIAqk3ThqvMEKJOCfD5HE8TNEPlnHI5czOGH0rcbg7yIkfAfRhCzumz5XGu5YAgxDDmgNkXMorplyCG+CiQTt/OhaQN6KKK0vQXkweIEE/Assem0CTJCPoOWCYT94Zm3nYNTXefJ8lDIFDSBI4/UwA97cBUC7snr62T740sBnNQDfXBRD/QaI/lKxdt1koNy0/8R6IQ2lUK/CcM9GgX5bhxa5OgKh6tOKKuRRvm3xyr6RejiP2oXpZjObGJxqZOKZCGHQa8jEw4RAE2w2KQcrZIwFPenIIEGufwiRqE7Mwh1ZyTufuJUXq4+TkQAAAB10RVh0dgB1Mjk0MC1wMS03LTljODg3YjZlZmE3NTYxZjN8AdvBAAAAAElFTkSuQmCC': 4,
    'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABkAAAAeCAYAAADZ7LXbAAACNUlEQVR4nLWWP2gTURzHP0nPJLXm0qEXIhx1OCoaRCiC6OAklCwRlAxCRSG4dHMoLjoJDgUHoUPAoYOLSxcRQeokKHTwzyAWFQoVD4k9CpcLkbt4SRwqpsl7l0vC+YVbvr8fv8+937v3uxdrO9UO/1mK1HUt9j5t0x61WtIgc0ojMRSkvom9sjw6ZO4BqftFARKXJv80RwcMkBwSJSEI0mw4kUKke+LVTMFL3v3C7OnxIPJ2CVpAOToeIBDimRvjVxwWIkpHSUcKcfB3+z2VeGp8iGTjPdqNfs/Ee7eJ1cPVOXJMZ7L/5EkUE2eXyY/bF2nsDPOOGpwok7lZYmZWDey9xLfwhwLs5/J5hdryZb69MPGHh4wjE3/tKt83LGlUhNSd7lRJnyOW6z7C5OuRhf+4QtUWI+KetMAHlAl5qaa9jf30IbXn8rMUL7/GKGghK5kIBgAkpg2yN1bJlovSePv9Fr/6wcHlBitTuMXhnCRgO/yOCgI6iZMSe8eMEhKgOZ1kZJDWFu5biZ/VwiHNuhN4qA6q9nINty76h+bz4RcJ780dqs9UUqVF1PN5Mn2Dsd202HtyD1v2CSeWmDqrCrb8tmKt41bWcSuwm5onNv23Aa5Jxxb/mvvSUK4vokmmtRxyUO4HOtWwJI1YYZXcgiaNhkNCpaNce0TuksFkQIYASeZLJM94eB9fQXNA7YSBcmGJ9JUiM/IF/JPkf9KVVzdpfDVp9bgqieMGU+nk0G0YCIlKfwBds6l+tDTJLAAAAB50RVh0dgB1Mjk0MC1wMS0zMy0wYjljYzM2NGVhNzgxMDI1LcJmeQAAAABJRU5ErkJggg==': 5,
    'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABkAAAAfCAYAAAASsGZ+AAADDklEQVR4nLWWTUhUURTHf+M48/yYLz9eKYpFk4sGkmYTgtAsCo3KIBjaFATuXES5qYXRQipIhAQRSUgQchNtxBYhQQVBQxYjRhb0ZaDTg+fn2JgzjjMtomzevc+ZMs/uvfu/53fuuefcey2pqJZmmy1vuwEA+bkKk4sfWQiFWHkxytpsnLQWBrsXS6kK5T7s++txHQngcYpzLdnSlZoLM3O7m9XxUNZA8lqe4T2q/t1KVsb7iHR1k05k9b+pmUK+T/QRudHN/6gKKSSljaB1mgCqzqA0BShUlZ/fqzqrL0PEX903hUj2ROfr1VN8e6cbpH7sF3qoalDlka1HWVpUcJcp2VeSmLhPTAJQrgxSUyc6+G1WF+4y+ZChT6LMDYtpsjRepmIzQBbLhOhPWXltlAQpDvqx/zPCAFl5GyZlVOwP4PJsgYBhT2JvhgSBZZ+PYiC1PM3soyFij8MktTCggurHdrARx7FmysUe3PCxUV3TRC4dJjaVKbC1TbCzZIjItZukTJuymvyz/VSc9FIoGf0jXTrJKVFgmRnJAvgZYPLuObSH02K6MyCrcakgca89C+CPIAduohmrPwOyrLNu6sBPfrCf8t4xqu6MUdnZj7KnWqIbJTYsFk8O94mK7UI/u04HKFFdFDldOHYHqLk+SHGtRP4kxLwppMCFVcaouYinwSVGY62m/ESLqE9MkjCkbGOuU+IIsBzw4ZHBAften2TOKMmvZhBUrBUSyGYNkKNlQGxeUZCKSMplU6vH6jGFKDj8Z8Q545MsmLhLfJiUlL0Xa4kpBIrq6sWzX+tm6XlcgtCZfTAg/q71U2x4TGTumyeA45BxD3TWetuZ+RTdiHo9ytzddmLvjQQVW1MA44NFvBn1UT63nScp63JPPZYCSM+HQDZe28WOjmbchl4QK1BtpPRss8QDsBgirZkACoI4zosAOQRwH+1CbQnKQTJTW3Hfuk6lpAUgy+MuqYeI9HQQf/dRLigIYA+2Unrcj1N6XOQA+WWpRJTlL5Mkor/+KOTX+HCqSk7v3JwgW7Uf9vIJrfooPLgAAAAddEVYdHYAdTI5NDAtcDEtNS1mNjBmZWMxMzlmYzc2YTYxLGCMKQAAAABJRU5ErkJggg==': 6,
    'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABkAAAAeCAYAAADZ7LXbAAAB0klEQVR4nNWWu0tCURzHv75upfhAuVHh5mRDFFEIgS7lWIu0FAVuDUFN7v0TIoFTUzgU1WI01FASgU53yCIIA8Esn/kora289x6999xrQb/tfPn9zoff4/w4mnYp+4lfNn3noZnlUHwq9eFaFsZpF0wkSCMVRiEa7wNkC5r9jW+Itg83Str/hWgWfbB3nlVNVy6Oh+1NfDQ7NCYIaySEYdOPpCKTErK7O3wAAO1qkAdQBamloqikcnzRHIJtgRX5KoO0ODxHwuDXmYVhPQCHTuyuCFI+DaOeF4iOICxzFqI/PaSewMue8MGyMKytwE7IQhHk9TiKpqDZcARhmR3oGkMHqSZQPDgXyfrlQNcsqCGFsyjehVmYQ7B4yb2gh9STKB2Ks9Au+YkTpQhSvYqhURaqARi9TslYmZAMCicxsTzph9UmHS0Pko6j9igUWTDzHhhlhMuC5C+PINqiTADGie5jSwdpcXi74MT6jAfWQVkMaUg7nSA0HDBMjYORx5CGFG4IpYIfjLv326CAZFC7JpRqxIch8UZXCMklUc8SdLcLVvmM3pDmHYc2Qde7nFT7qKdv5T5BUFnoxihq1RuSQ+OW0A94YBilYqj8rci0P/ncfQFZgoA8RmcsKwAAAB10RVh0dgB1Mjk0MC1wMS05LWEyOGI5ZjJlZTk5NGRiZDcpqOmgAAAAAElFTkSuQmCC': 7,
    'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABkAAAAfCAYAAAASsGZ+AAADS0lEQVR4nLWWX2hTVxzHPzeNuenyx9HulsRmEVa2lTyMBqF0FCY+2O3B+NSHCYLQh8H2oA7CChujENbBJDJhk0IZexj0YdIxxL0sL0VhLOpDxD9BlE5xNxq8aeeSxTRJk/hWe885N7EMf0+Xe37n9+H3O9/f7xytXS52eMnmetkAAHcvh0YxR2klQ/3PPK3qKp2KjhaKoA3H8Y5P4Z+MsdvTPYbmVK5NK8vD019Q/8vsHsEzgvvgPMbROP6+HUBq1xconDpDp9E9vs1G0xhzCV5VgOQzsTIUdwoAuJ2ktJijplgSIHWsn1NsKgDaeJrBs1eJ/nSV8HyaXYOyT2flG0p3e0FaeWpZS/YaWyScTDBgBNG9QfxvJojOpRVlyFG/nO8BWTdpSlkY6If24xM3hqYITCqyuWPyX1eI0uK4w6r/Ov1vT/XeLkECBrI4ynRUpwk0S7K8tbci+LtCvHF87xmCS5aNKyZtMVorT3VFrP9++g/EJLBQLp3B6VncQge3zyX5+w+LzS2AyaNvU2xUhCwOnyQ8LDF22IyBCTQfdNazYFsz0D74juGZOP0yo8tYKWQwv07RtBSStoET6J/Msmef4TgIndXlCdIXlesrWbNMp2BSazm7KDKps3YuyfpypjdguxkzBL6cJRTqCalT+uEY/2RyYgS0sY/xvz9CH9BazVD9bYn2huDmncZ/ep6wIFAbpHF9gQdfncGeWhzPp4u8/m7QVtt2JYf52YfU1wTQ2CJ7PrdPiG37yqydFwHA5EmGBACAKxAncmIWTfS/tsSTguC79bWRp35D3AG7xtWyBHCNTuCRbsWLNG7ZFfkcUrFQCcTl0x0QAAbuvfLf1mMniIO1n5SdF1smTcX9gTfoABmIKJupeTFL1YFRu5JBdYG6h5wgfTFekYYjcCPF4+VVngq13CxcoHj2RwViGv0dO8Qm4XbxAveOJ+WJCxBI4JmMoQGd+8s0bq+qvNAO/8obR2O2c5A6/t9LKazvl2Qpv4iNphmaS7BbuJSUA/LpzSUenUrJHe1oBtqBNKGPJpRvL8cpTMvC+mWB8u8Z2hWnSRzBtW+GwJEEr0Xlhu0N2WaNapnawzyNLTXruKMj+AaCeBxejTuG/F97BlGUQSwGRtVmAAAAHXRFWHR2AHUyOTQwLXAxLTMtZWY5YTE5NGY0ZDg4YTUyM3JmzJgAAAAASUVORK5CYII=': 8,
    'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABkAAAAfCAYAAAASsGZ+AAADEklEQVR4nLWWX0hTcRTHP1fXdNV0/bm2ckV4IcoiCl8mUfa0twWBSKAk+RISRQ9hD4GBTw2EjIjeDKFeIuhBglj54FMjCgsqpBqVzJpe0jlberfdrYcovPf3292yOm/3e875fX5/zu93j1JIJ4v8Z6v63wAAV7mAfCrOfCzG96dRcjM6RT0OviBKoBnP4TB1R5rxVjuPoZTcLlNHvz1A6kHUeQR3EHfvII2H1JIzlkMyE0z1ncXQdWfAb1NxdYzgb9fwSLzimZgJPkf+BACgk7/bzcwTQ+oVIIuPImQmJQC1ndreEXwXR6jv6kFxi6DcjZvoy2KqdbvMCaa6T2BkbVG7B2m4HKZ+xQEXkqN8unCBvC22qmsM7Vig9EoKr2MigDbWnrYCAKr8YTZ0tAmzLjyOMW/TLJCFtzEhCX+ItY2iDOBrDYv7nRxnybbblhgzJYHs0aiXM0DVcHvtYpTse2sBlL/xWYN8SadKtV9UzTnrUspD4gkypXxmgtw7US58cYDU7giLGck7fJuUM5aeRhHqRGIWyPq9QcnS3rB8bYhZ22Hmp0dJ3hiuAGF/IBtDrDswxOIL24hfb7JwZpT0vhDugEoxESX7aqIiAAhnUkdDz0Vcwm0GSFB8NYzxMLICoII01hHy85L5+85Lng3RlNB16o9KdJ/qDAHw7O9l59URapoCMjcQoKr9PttOaRRmRa+roc76XWqWLjXIjitjZFNx0vE4xssEhW0atYEAnl0a690ACeaT9sxmqrdWCPllbp/G5hYNWiTOxTg5AdJGbZNV+at/fOZZlJxdPBQUH9NVE8w3zN29ZxNV3K0HhYJbHcRMo98aYPmrTd/Ug7elRggXIXqUD/3DzH5MkzXF8Y3pGFOXjpOK2i+jypqTnWyUdC6SgzcoTEZY6IuwgAqqhvIrMRWjKPm9ws87s6VVXEUJyErTQdcp22LuHkQ9dVDaqVQAKWcqSms/m8+FhIpyhng1PC1tZJ6POwweQNnXzrquTrY01ZWtHocO0mBpLkFmyrpdyiYN73aVmjKtaWWQf2g/APNlCsGuIPJrAAAAHXRFWHR2AHUyOTQwLXAxLTEtYTJmNTZiYzZjNGVmOGM5Yer3pTsAAAAASUVORK5CYII=': 9,


}


headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://match.yuanrenxue.cn/match/4",
    "sec-ch-ua": '"Not:A-Brand";v="8", "Chromium";v="156", "Google Chrome";v="156"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "yuanrenxue",
    "x-requested-with": "XMLHttpRequest",
}

cookies = {
    "Hm_lvt_f80b2b389f44bbfb3bfe1704817d44e0": "1793624216",
    "HMACCOUNT": "08BEF2A03FF17943",
    "m": "1b52258c299ef7d6fdb3bdd992294702|1793624413830",
    "Hm_lvt_434c501fe98c1a8ec74b813751d4e3e3": "1793883313",
    "Hm_lpvt_434c501fe98c1a8ec74b813751d4e3e3": "1793883482",
    "sessionid": "bp8g2t506i2t9wiiu4ore8asfkyb356r",
    "Hm_lpvt_f80b2b389f44bbfb3bfe1704817d44e0": "1794313147",
}

params = {
    "page": "2",
    "pageSize": "10",
    "kw": "",
}

USE_CHARLES = False
IMG_WIDTH = 8.5


def fetch(page=2):
    client_kwargs = {
        "http2": True,
        "cookies": cookies,
        "trust_env": False,
        "timeout": httpx.Timeout(10.0, connect=10.0),
    }
    if USE_CHARLES:
        client_kwargs["proxy"] = "http://127.0.0.1:8888"
        client_kwargs["verify"] = "charles.pem"
    with httpx.Client(**client_kwargs) as client:
        response = client.get(url, headers=headers, params={**params, "page": str(page)})
        response.raise_for_status()
        return response.json()


def hidden_class(data):
    # 页面 JS: hex_md5(btoa(res.key + res.value).replace(/=/g, '')) -> display:none
    seed = base64.b64encode((data["key"] + data["value"]).encode()).decode().replace("=", "")
    return hashlib.md5(seed.encode()).hexdigest()


def png_fingerprint(src):
    # 每张图的 tEXt 元数据都不同，去掉该块后相同数字的图片内容完全一致
    raw = base64.b64decode(src.split("base64,", 1)[1])
    stripped = bytearray(raw[:8])
    pos = 8
    while pos + 12 <= len(raw):
        size = int.from_bytes(raw[pos:pos + 4], "big")
        chunk = raw[pos:pos + 12 + size]
        if raw[pos + 4:pos + 8] != b"tEXt":
            stripped += chunk
        pos += 12 + size
    return hashlib.md5(stripped).hexdigest()


num_by_png = {png_fingerprint(src): num for src, num in base64_to_num.items()}


def parse_info(data):
    hidden = hidden_class(data)
    rows = []
    for td in re.findall(r"<td>(.*?)</td>", data["info"], re.S):
        visible = []
        for tag in re.findall(r"<img[^>]+>", td):
            class_match = re.search(r'class="img_number ([^"]+)"', tag)
            if class_match and class_match.group(1) == hidden:
                continue
            left = float(re.search(r"left:(-?[\d.]+)px", tag).group(1))
            src = re.search(r'src="([^"]+)"', tag).group(1)
            # .img_number 为 position:relative、width:8.5px，隐藏标签不占位
            visible.append({"x": len(visible) * IMG_WIDTH + left, "src": src})
        rows.append(sorted(visible, key=lambda cell: cell["x"]))
    return rows


def parse_numbers(data):
    numbers = []
    for row in parse_info(data):
        digits = "".join(str(num_by_png[png_fingerprint(cell["src"])]) for cell in row)
        numbers.append(int(digits))
    return numbers


if __name__ == "__main__":
    # pages = [int(sys.argv[1])] if len(sys.argv) > 1 else range(1, 6)
    total = 0
    for page in range(1, 6):
        numbers = parse_numbers(fetch(page))
        print(f"page {page}: {numbers}")
        total += sum(numbers)
    print(f"sum: {total}")
