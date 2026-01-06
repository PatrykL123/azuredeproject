class reusable:
    def dropCols(self, df, columns):
        df = df.drop(*columns)
        return df

    
        