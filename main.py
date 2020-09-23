#%%
import json
import random

# %%
class fake_data:
  def __init__(self, samples_file, tables_file):
    file_samples = open("./samples.json")
    self.samples = json.load(file_samples)

    file_tables = open("./tables.json")
    self.tables = json.load(file_tables)
    pass

  def __random_number(self, min, max):
    return str(random.randint(min, max))
    pass

  def __random_char(self, chars, count):
    result = ""
    for i in range(random.randint(int(count[0]), int(count[1]))):
      result += chars[random.randrange(0, len(chars))]
      pass
    return result

  def __random_data(self, data):
    return data[random.randrange(len(data))]
    pass

  def __format(self, format):
    result = ""
    special_chars = {
      "<": "range",
      "[": "chars",
      "@": "sample"
    }
    states = {
      "normal": { "index": 0 },
      "range": { "index": 1, "end": ">" },
      "chars": { "index": 2, "end": "]" },
      "sample": { "index": 3, "end": ";" }
    }
    state = "normal"
    state_string = ""
    backslash = False

    for ch in format:
      if not backslash:
        if states[state]["index"] == 0:
          if ch in special_chars:
            state_string = ""
            state = special_chars[ch]
            ch = ""
            pass
        elif states[state]["end"] == ch:
          if (state in states) and (states[state]["index"] == 1):
            number_range = state_string.split(",")
            ch = self.__random_number(int(number_range[0]), int(number_range[1]))
            pass
          elif (state in states) and (states[state]["index"] == 2):
            chars = ""
            count = ["10", "10"]
            char_list = state_string.split(":")[0]
            if state_string.find(":") >= 0:
              count = state_string.split(":")[1].split(",")
              if len(count) == 1:
                count.append(count[0])
                pass
              pass
            last_dash = 0
            while char_list.find("-", last_dash) >= 0:
              dash_pos = char_list.index("-", last_dash)
              chars += char_list[last_dash + 1:dash_pos - 1]
              if char_list[dash_pos - 1] != "\\":
                start = char_list[dash_pos - 1]
                end = char_list[dash_pos + 1]
                for char in range(ord(start), ord(end) + 1):
                  chars += chr(char)
                  pass
                pass
              else:
                chars += "-"
                pass
              last_dash = dash_pos + 1
              pass
            ch = self.__random_char(chars, count)
            pass
          elif (state in states) and (states[state]["index"] == 3):
            path = state_string.split(".")
            data = self.samples
            for item in path:
              data = data[item]
              pass
            ch = self.__random_data(data)
            pass
          state = "normal"
          pass
        pass

      if backslash or states[state]["index"] == 0:
        if not backslash:
          if ch == "\\":
            backslash = True
            pass
        else:
          backslash = False
          ch = ""
          pass
        result += ch
        
      else:
        state_string += ch
        pass
      pass

    return result

  def __table(self, out, tableName):
    table = self.tables[tableName]
    if tableName in out:
      return out[tableName]
      pass
    else:
      rowCount = 10
      result = []

      if "count" in table:
        rowCount = table["count"]
        pass
      
      for i in range(rowCount):
        row = {}
        if "relations" in table:
          for relation in table["relations"]:
            out[table["relations"][relation]["table"]] = self.__table(out, table["relations"][relation]["table"])
            row[relation] = self.__random_data(out[table["relations"][relation]["table"]])[table["relations"][relation]["field"]]
            pass
          pass

        for field in table["fields"]:
          accepted = False
          while not accepted:
            field_value = self.__format(table["fields"][field]["format"])
            accepted = ("unique" not in table["fields"][field]) or (not table["fields"][field]["unique"])
            if not accepted:
              accepted = True
              i = 0
              while accepted and i < len(result):
                if result[i][field] == field_value:
                  accepted = False
                  pass
                i += 1
                pass
              pass
            pass
          if table["fields"][field]["type"] == "number":
            row[field] = int(field_value)
            pass
          else:
            row[field] = field_value
            pass
          pass

        result.append(row)
        pass
      pass
    return result

  def generate(self):
    result = {}

    for table in self.tables:
      result[table] = self.__table(result, table)
      pass
    return result
  pass

# %%
if __name__ == "__main__":
  fd = fake_data("./samples.json", "tables.json")
  print(json.dumps(fd.generate(), ensure_ascii=True, indent=2))
  pass
