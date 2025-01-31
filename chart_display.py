import pandas as pd
import plotly.graph_objects as go


class IndicatorMerger:
    def __init__(self, df1, df2, recession_periods, datasets_info):
        self.df1 = df1
        self.df2 = df2
        self.recession_periods = recession_periods
        self.datasets_info = datasets_info

    def merge_dataframes(self):
        df_merged = pd.merge(self.df1.set_index('Date'), self.df2.set_index(
            'Date'), left_index=True, right_index=True, how='left')
        df_merged = df_merged.bfill().combine_first(df_merged.ffill())
        df_merged.index = pd.to_datetime(df_merged.index)
        return df_merged

    def get_display_name(self, series_id):
        if series_id not in self.datasets_info['Series_Id'].values:
            return series_id
        return self.datasets_info.loc[self.datasets_info['Series_Id'] == series_id, 'Display_Name'].values[0]

    def create_chart(self, df_merged):
        value1 = df_merged.columns[0]
        value2 = df_merged.columns[1]

        display_name1 = self.get_display_name(value1)
        display_name2 = self.get_display_name(value2)

        trace1 = go.Scatter(
            x=df_merged.index,
            y=df_merged[value1],
            mode='lines',
            name=display_name1,
            line=dict(color='#1b4cb5', width=2)
        )

        trace2 = go.Scatter(
            x=df_merged.index,
            y=df_merged[value2],
            mode='lines',
            name=display_name2,
            line=dict(color='#c9617e', width=2),
            yaxis='y2'
        )

        fig = go.Figure()

        fig.add_trace(trace1)
        fig.add_trace(trace2)

        for start, end in self.recession_periods:
            fig.add_vrect(
                x0=start, x1=end,
                fillcolor="grey", opacity=0.2,
                layer="below", line_width=0
            )

        fig.update_layout(
            title=f'Comparison between {display_name1} and {
                display_name2} with Recession Periods',
            titlefont=dict(family='Roboto', size=16, color='#4B4B4B'),
            xaxis=dict(
                title='Date',
                titlefont=dict(size=14, family='Roboto', color='#4B4B4B'),
                tickfont=dict(size=12, color='#4B4B4B')
            ),
            yaxis=dict(
                title=f'{display_name1} Value',
                titlefont=dict(size=14, family='Roboto', color='#1b4cb5'),
                tickfont=dict(size=12, color='#1b4cb5'),
                gridcolor='rgba(0,0,0,0)'
            ),
            yaxis2=dict(
                title=f'{display_name2} Value',
                titlefont=dict(size=14, family='Roboto', color='#c74256'),
                tickfont=dict(size=12, color='#c74256'),
                overlaying='y',
                side='right',
                gridcolor='rgba(0,0,0,0)'
            ),
            showlegend=True,
            legend=dict(x=0.1, y=0.9),
            plot_bgcolor='white',
            width=800,
            height=600
        )

        fig.update_layout(margin=dict(l=40, r=40, t=80, b=40))
        return fig

    def run(self):
        df_merged = self.merge_dataframes()
        fig = self.create_chart(df_merged)
        fig.show()
