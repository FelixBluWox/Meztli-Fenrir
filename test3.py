import argparse

p = argparse.ArgumentParser()
p.add_argument('guild_id', type=int)
p.add_argument('bot_type', default='Fenrir', type=str)
p.add_argument('-n', dest='number', default=0, type=int)

args = p.parse_args()

print(vars(args))

print(args.guild_id)
print(args.bot_type)
print(args.number)