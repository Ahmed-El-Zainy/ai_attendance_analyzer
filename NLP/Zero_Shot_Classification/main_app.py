class MainApplication:
    """
    A class used to run queries on data using a query processor and a language model.

    ...

    Attributes
    ----------
    data_loader : DataLoader
        a DataLoader object to load the data
    query_processor : QueryProcessor
        a QueryProcessor object to process the queries
    llm : LLM
        a LLM object to generate text

    Methods
    -------
    run_query(query):
        Runs a query on the data and returns the result.
    """

    def __init__(self, data_loader, query_processor, llm):
        """
        Constructs all the necessary attributes for the MainApplication object.

        Parameters
        ----------
            data_loader : DataLoader
                a DataLoader object to load the data
            query_processor : QueryProcessor
                a QueryProcessor object to process the queries
            llm : LLM
                a LLM object to generate text
        """

        self.data_loader = data_loader
        self.query_processor = query_processor
        self.llm = llm

    def run_query(self, query):
        """
        Runs a query on the data and returns the result.

        Parameters
        ----------
            query : str
                a string representing the query

        Returns
        -------
        str
            a string representing the result of the query

        Raises
        ------
        ValueError
            If the data could not be loaded.
        """

        # Load data once when running the query
        self.data_loader.load_data()
        data = self.data_loader.get_data()

        # Ensure the data is loaded correctly
        if data is None:
            raise ValueError(
                "Data could not be loaded. Please check the file path and format."
            )

        self.query_processor.set_data(
            data
        )  # Pass the loaded data to the query processor
        response = self.query_processor.process_query(query)
        return response
