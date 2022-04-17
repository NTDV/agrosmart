import asyncio
import json
from nextion import Nextion, EventType

SETTINGS_PATH = '/home/pi/main/static/data/settings.json'
UPDATE_PATH = '/home/pi/main/static/data/update.json'


def toRichNum(n):
    if int(n) < 10:
        return '0' + str(n)
    else:
        return str(n)


class App:
    def __init__(self):
        self.client = Nextion('/dev/ttyS0', 9600, self.event_handler, encoding='iso-8859-5')

    async def event_handler(self, type_, data):
        try:
            if type_ == EventType.TOUCH:
                print(data)
                settings = {}
                with open(SETTINGS_PATH, encoding='utf-8') as settingsFile:
                    settings = json.load(settingsFile)

                if data.page_id == 0:
                    if data.component_id == 21:
                        await self.client.command('page 1')
                        
                        h, m = map(int, settings['r1b'].split(':'))
                        await self.client.set('n0.val', h)
                        await self.client.set('n1.val', m)
                        
                        h, m = map(int, settings['r1e'].split(':'))
                        await self.client.set('n2.val', h)
                        await self.client.set('n3.val', m)
                        
                        h, m = map(int, settings['r2b'].split(':'))
                        await self.client.set('n4.val', h)
                        await self.client.set('n5.val', m)
                        
                        h, m = map(int, settings['r2e'].split(':'))
                        await self.client.set('n6.val', h)
                        await self.client.set('n7.val', m)
                        
                        h, m = map(int, settings['r3b'].split(':'))
                        await self.client.set('n8.val', h)
                        await self.client.set('n9.val', m)
                        
                        h, m = map(int, settings['r3e'].split(':'))
                        await self.client.set('n10.val', h)
                        await self.client.set('n11.val', m)
                    elif data.component_id == 3:
                        settings['r1'] = '-1'
                    elif data.component_id == 4:
                        settings['r1'] = '0'
                    elif data.component_id == 5:
                        settings['r1'] = '1'
                    elif data.component_id == 7:
                        settings['r2'] = '-1'
                    elif data.component_id == 8:
                        settings['r2'] = '0'
                    elif data.component_id == 9:
                        settings['r2'] = '1'
                    elif data.component_id == 11:
                        settings['r3'] = '-1'
                    elif data.component_id == 12:
                        settings['r3'] = '0'
                    elif data.component_id == 13:
                        settings['r3'] = '1'
                elif data.page_id == 1:
                    if data.component_id == 2:
                        settings['r1b'] = toRichNum(await self.client.get('n0.val')) + ':' + toRichNum(await self.client.get('n1.val'))
                        settings['r1e'] = toRichNum(await self.client.get('n2.val')) + ':' + toRichNum(await self.client.get('n3.val'))

                        settings['r2b'] = toRichNum(await self.client.get('n4.val')) + ':' + toRichNum(await self.client.get('n5.val'))
                        settings['r2e'] = toRichNum(await self.client.get('n6.val')) + ':' + toRichNum(await self.client.get('n7.val'))

                        settings['r3b'] = toRichNum(await self.client.get('n8.val')) + ':' + toRichNum(await self.client.get('n9.val'))
                        settings['r3e'] = toRichNum(await self.client.get('n10.val')) + ':' + toRichNum(await self.client.get('n11.val'))
                        
                        await self.client.command('page 0')
                    elif data.component_id == 54:
                        await self.client.command('page 2')
                        
                        await self.client.set('n0.val', int(settings['co2b']))
                        await self.client.set('n2.val', int(settings['co2e']))
                        
                        await self.client.set('n4.val', int(settings['humb']))
                        await self.client.set('n6.val', int(settings['hume']))
                        
                        await self.client.set('n8.val', int(settings['temb']))
                        await self.client.set('n10.val', int(settings['teme']))
                        
                elif data.page_id == 2:
                    if data.component_id == 1:
                        await self.client.command('page 1')
                        
                        h, m = map(int, settings['r1b'].split(':'))
                        await self.client.set('n0.val', h)
                        await self.client.set('n1.val', m)
                        
                        h, m = map(int, settings['r1e'].split(':'))
                        await self.client.set('n2.val', h)
                        await self.client.set('n3.val', m)
                        
                        h, m = map(int, settings['r2b'].split(':'))
                        await self.client.set('n4.val', h)
                        await self.client.set('n5.val', m)
                        
                        h, m = map(int, settings['r2e'].split(':'))
                        await self.client.set('n6.val', h)
                        await self.client.set('n7.val', m)
                        
                        h, m = map(int, settings['r3b'].split(':'))
                        await self.client.set('n8.val', h)
                        await self.client.set('n9.val', m)
                        
                        h, m = map(int, settings['r3e'].split(':'))
                        await self.client.set('n10.val', h)
                        await self.client.set('n11.val', m)
                    elif data.component_id == 2:
                        settings['co2b'] = await self.client.get('n0.val')
                        settings['co2e'] = await self.client.get('n2.val')

                        settings['humb'] = await self.client.get('n4.val')
                        settings['hume'] = await self.client.get('n6.val')

                        settings['temb'] = await self.client.get('n8.val')
                        settings['teme'] = await self.client.get('n10.val')
                        
                        await self.client.command('page 0')
                with open(SETTINGS_PATH, 'w', encoding='utf-8') as settingsFile:
                    json.dump(settings, settingsFile, ensure_ascii=False, indent=4)
        except e:
            print('Can not process click')
            print(e)

    async def run(self):
        await self.client.connect()

        while True:
            try:
                page = await self.client.get('dp')
                if page == 0:
                    with open(SETTINGS_PATH, encoding='utf-8') as settingsFile:
                        settings = json.load(settingsFile)
                        with open(UPDATE_PATH, encoding='utf-8') as updateFile:
                            data = json.load(updateFile)

                            await self.client.set('t18.txt', str(round(float(data['upt']), 1)) + ' часов')
                            await self.client.set('t11.txt', data['dat'] + ' ' + data['tim'])

                            await self.client.set('t19.txt', data['cod'])
                            await self.client.set('t20.txt', str(round(float(data['volt']), 2)))
                            await self.client.set('t21.txt', data['cpu'] + ' C')

                            if settings['r1'] == '-1':
                                await self.client.set('b0.bco', 31)
                                await self.client.set('b1.bco', 65535)
                                await self.client.set('b2.bco', 65535)
                            elif settings['r1'] == '0':
                                await self.client.set('b0.bco', 65535)
                                await self.client.set('b1.bco', 31)
                                await self.client.set('b2.bco', 65535)
                            else:
                                await self.client.set('b0.bco', 65535)
                                await self.client.set('b1.bco', 65535)
                                await self.client.set('b2.bco', 31)

                            if settings['r2'] == '-1':
                                await self.client.set('b3.bco', 31)
                                await self.client.set('b4.bco', 65535)
                                await self.client.set('b5.bco', 65535)
                            elif settings['r2'] == '0':
                                await self.client.set('b3.bco', 65535)
                                await self.client.set('b4.bco', 31)
                                await self.client.set('b5.bco', 65535)
                            else:
                                await self.client.set('b3.bco', 65535)
                                await self.client.set('b4.bco', 65535)
                                await self.client.set('b5.bco', 31)

                            if settings['r3'] == '-1':
                                await self.client.set('b6.bco', 31)
                                await self.client.set('b7.bco', 65535)
                                await self.client.set('b8.bco', 65535)
                            elif settings['r1'] == '0':
                                await self.client.set('b6.bco', 65535)
                                await self.client.set('b7.bco', 31)
                                await self.client.set('b8.bco', 65535)
                            else:
                                await self.client.set('b6.bco', 65535)
                                await self.client.set('b7.bco', 65535)
                                await self.client.set('b8.bco', 31)

                            await self.client.set('t7.txt', 'низкий' if data['wat'] else 'высокий')

                            co2 = int(data['co2']['co2'])
                            await self.client.set('t8.txt', str(co2) + ' ppm')
                            if co2 >= int(settings['co2e']):
                                await self.client.set('t12.txt', 'X')
                                await self.client.set('t12.pco', 63488)
                            elif co2 <= int(settings['co2b']):
                                await self.client.set('t12.txt', '!')
                                await self.client.set('t12.pco', 65504)
                            else:
                                await self.client.set('t12.txt', 'Ok')
                                await self.client.set('t12.pco', 2016)

                            hum = int(data['hum'])
                            await self.client.set('t9.txt', str(hum) + ' %')
                            if hum >= int(settings['hume']):
                                await self.client.set('t13.txt', 'X')
                                await self.client.set('t13.pco', 63488)
                            elif hum <= int(settings['humb']):
                                await self.client.set('t13.txt', '!')
                                await self.client.set('t13.pco', 65504)
                            else:
                                await self.client.set('t13.txt', 'Ok')
                                await self.client.set('t13.pco', 2016)

                            tmp = int(data['tmp'])
                            await self.client.set('t10.txt', str(tmp) + ' C')
                            if tmp >= int(settings['teme']):
                                await self.client.set('t14.txt', 'X')
                                await self.client.set('t14.pco', 63488)
                            elif tmp <= int(settings['temb']):
                                await self.client.set('t14.txt', '!')
                                await self.client.set('t14.pco', 65504)
                            else:
                                await self.client.set('t14.txt', 'Ok')
                                await self.client.set('t14.pco', 2016)
            except:
                print('Cannot update display')

        print('finished')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app = App()
    asyncio.ensure_future(app.run())
    loop.run_forever()
